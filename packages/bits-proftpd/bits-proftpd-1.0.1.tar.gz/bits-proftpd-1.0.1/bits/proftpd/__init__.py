# -*- coding: utf-8 -*-
"""ProFTPD class file."""

import datetime
import nis
import os
import re
import subprocess


class ProFTPD(object):
    """ProFTPD class."""

    def __init__(
        self,
        config_file,
        disable_sites=[],
        removed_config_file='removed.conf',
        remove_inactive=False,
    ):
        """Initialize an ProFTPD class instance."""
        self.config_file = config_file
        self.removed_config_file = removed_config_file

        self.disable_sites = disable_sites
        self.remove_inactive = remove_inactive

        self.deactivate = set()
        self.nofilesystem = set()

    def audit_config(self):
        """Audit the config."""
        config = self.get_ftp_config()

        active = config['active']
        inactive = config['inactive']

        print('Active FTP Sites: {}'.format(len(active)))
        self.root_stats(active)

        print('\nInactive FTP Sites: {}'.format(len(inactive)))
        self.root_stats(inactive)

        count = self.check_filesystems(active)
        print('\nActive FTP Sites Referencing Non-Existent Filesystems: {}'.format(count))
        print('   {}'.format('\n   '.join(sorted(self.nofilesystem))))

        count = self.check_users(active)
        print('\nActive FTP Sites Referencing Terminated Users: {}'.format(count))

        count = self.check_expires(active)
        print('\nActive FTP Sites Past Expiration: {}'.format(count))

        print('\nFTP Sites to Deactivate: {}'.format(len(self.deactivate)))
        for p in sorted(self.deactivate):
            print('   - {}'.format(p))

        count = 0
        remaining = []
        for a in sorted(active):
            if a not in self.deactivate:
                count += 1
                remaining.append(a)

        total = 0
        files = 0
        print('\nActive FTP Sites Remaining ({}):'.format(count))
        for a in remaining:
            if a in [
                # '/xchip/obelix/ftp/lincs/',
            ]:
                print('   * skipping {}'.format(a))
                continue
            # get number of files
            output = subprocess.Popen('sudo find {} -type f | wc -l'.format(a), shell=True, stdout=subprocess.PIPE).communicate()[0]
            dirfiles = output.rstrip().split()[0]

            # get directory size
            output = subprocess.Popen('sudo du -sk '+a, shell=True, stdout=subprocess.PIPE).communicate()[0]
            dirsize = output.rstrip().split()[0]

            files += int(dirfiles)
            total += int(dirsize)

            print('   * {} ({} files using {}k)'.format(a, dirfiles, dirsize))

        print('Total Files: {}'.format(files))
        print('Total Volume Shared: {} GB'.format(total/1024/1024))

    def check_expires(self, active):
        """Check expire dates."""
        count = 0
        today = str(datetime.date.today())
        date = None
        for a in sorted(active):
            e = active[a]
            v = self.get_value('#+ remov(e|al)( date|)(:|)', e)
            if v:
                if re.search('....-..-..', v):
                    date = v.split()[2]
                elif re.search('../../....', v):
                    m, d, y = v.split()[2].split('/')
                    date = '-'.join([y, m, d])
                else:
                    continue
            if date and date < today:
                count += 1
                self.deactivate.add(a)
        return count

    def check_filesystems(self, active):
        """Check filesystems to be deactivated."""
        count = 0
        for a in sorted(active):
            # nodir = False
            # noparent = False
            if not os.path.isdir(a):
                # nodir = True
                count += 1
                self.deactivate.add(a)
                self.nofilesystem.add(a)
                # p = '/'.join(a.split('/')[:-2])
                # if not os.path.isdir(p):
                #     noparent = True
                # if nodir and noparent:
                # 	print '  - '+a+' (no dir)'
                # elif nodir:
                # 	print '  - '+a+' (no dir or parent)'
            # else:
            # 	print '   + '+a
        return count

    def check_missing_filesystems(self, entries):
        """Check for existence of filesystems."""
        missing = []
        for a in sorted(entries):
            if not os.path.isdir(a):
                missing.append(a)
        return missing

    def check_users(self, active):
        """Check Users."""
        count = 0
        for a in sorted(active):
            e = active[a]
            v = self.get_value('User', e)
            try:
                n = nis.match(v, 'passwd')
                if re.search(':NoLogin', n):
                    count += 1
                    self.deactivate.add(a)
                    # print '   - '+a+' ('+v+')'
            except nis.error as error:
                print('{}: {}'.format(error.message, v))
        return count

    def disable_entry(self, e):
        """Disable a single entry."""
        disabled = []
        start = True
        today = datetime.date.today().strftime('%Y-%m-%d')
        for a in e:
            if not a and start:
                disabled.append('')
                disabled.append('# ----- DISABLED by proftpd-cli on {} ----- #'.format(today))
                start = False
            elif not a:
                disabled.append('#')
            elif a[0] != '#':
                disabled.append('# '+a)
            else:
                disabled.append(a)
        return disabled

    def get_ftp_config_lines(self):
        """Return the current contents of the config file."""
        lines = []
        f = open(self.config_file, 'r')
        for line in f.xreadlines():
            if line:
                lines.append(line.replace('    ', ' ').strip())
        return lines

    def get_ftp_config(self, n=0):
        """Return the current entries in the config."""
        lines = self.get_ftp_config_lines()

        all_entries = []

        active_entries = {}
        inactive_entries = {}

        header = []
        if n == 0:
            header = self.get_header(lines)
            n = len(header)

        # get the current line number to start reading from
        line = lines[n]

        comments = []

        while n < len(lines)-1:

            # if the current line is <Anonymous, read until the </Anonymous>
            if re.search(r'^<Anonymous ', line):
                path = line.replace('<Anonymous ', '').replace('>', '').strip()
                # start of an active entry
                entry = comments
                comments = []
                while not re.search('^</Anonymous>', line):
                    entry.append(line)
                    n += 1
                    line = lines[n]
                entry.append(line)
                n += 1
                line = lines[n]
                # add to all_entries and active_entries
                all_entries.append([path, entry])
                active_entries[path] = entry

            # if the current line is #<Anonymous, read until the #</Anonymous
            elif re.search(r'^# <Anonymous ', line):
                path = line.replace('# <Anonymous ', '').replace('>', '').strip()
                # start of an inactive (commented) entry
                entry = comments
                comments = []
                while not re.search('^# </Anonymous>', line):
                    entry.append(line)
                    n += 1
                    line = lines[n]
                entry.append(line)
                n += 1
                line = lines[n]
                # add to all_entries and inactive_entries
                all_entries.append([path, entry])
                inactive_entries[path] = entry

            else:
                if line:
                    comments.append(line)
                n += 1
                line = lines[n]

        if line:
            comments.append(line)

        data = {
            'header': header,
            'active': active_entries,
            'inactive': inactive_entries,
            'all': all_entries,
            'footer': comments,
        }

        return data

    def get_header(self, lines):
        """Get the configuration header."""
        n = 0
        line = lines[n]
        header = []
        while not re.search(r'^<Anonymous ', line):
            header.append(line)
            n += 1
            line = lines[n]
        return header

    def get_value(self, name, entry):
        """Get a single value."""
        for l in entry:
            check = '^{} '.format(name)
            if re.search(check, l):
                return(l.replace('{} '.format(name), '').strip())

    def process_active(self, e):
        """Process an active entry."""
        output = []
        comment = False
        indent = 0
        for line in e:
            line = line.strip()

            # check if this line is a comment
            if re.search('^#', line):
                # check if the previous line was not a comment
                if not comment:
                    output.append('')
                comment = True
            else:
                comment = False

            # check if this line is a close tag
            if re.search(r'^</Anonymous>', line):
                output.append('')
                indent -= 2
            elif re.search(r'^</Directory>', line):
                indent -= 2
            elif re.search(r'^</Limit>', line):
                indent -= 2

            c = line.split()

            # if this is a comment or a tag, print it as usual
            if re.search("^(#|<)", line):
                output.append(' '*indent + line)

            # if it has more than one word, print it with ljust
            elif len(c) > 1:
                output.append(' '*indent + c[0].ljust(24) + ' '.join(c[1:]))

            # if it is just a single word (AllowAll, DenyAll), print it out
            elif c:
                output.append(' '*indent + line)

            # else ignore empty lines

            # check if this line is an open tag
            if re.search(r'^<Limit ', line):
                indent += 2
            elif re.search(r'^<Directory ', line):
                indent += 2
            elif re.search(r'^<Anonymous ', line):
                indent += 2

        return output

    def process_config(self, config):
        """Process all entries in a config file."""
        header = config['header']
        entries = config['all']
        active = config['active']
        footer = config['footer']

        output = []
        # process the header, content and footer
        output += self.process_header(header)
        output += self.process_entries(entries)
        output += self.process_header(footer)

        print('Missing filesystems:')
        missing = self.check_missing_filesystems(active)
        for path in sorted(missing):
            print(path)

        return output

    def process_entries(self, entries):
        """Process the entries in a config."""
        output = []
        removed = []
        for _, e in entries:
            o, r = self.process_entry(e)
            output += o
            removed += r

        if removed:
            f = open(self.removed_config_file, 'w')
            f.writelines('\n'.join(removed))

        return output

    def process_entry(self, e):
        """Process a single entry."""
        header = []
        output = []
        removed = []
        # today = datetime.date.today().strftime('%Y-%m-%d')
        expire_date = None
        # last = None
        for line in e:
            # comment = False
            start = False

            # check commented entries
            if re.search(r'^# <Anonymous ', line):
                start = True
                if self.remove_inactive:
                    removed += self.process_inactive(e)
                else:
                    output += self.process_inactive(e)
                break

            # check active entries
            elif re.search(r'^<Anonymous ', line):
                # comment = False
                start = True
                path = '/{}/'.format('/'.join(line.split('/')[1:-1]))
                if path in self.disable_sites:
                    output = self.disable_entry(self.process_active(e))
                else:
                    output += self.process_active(e)
                break

            else:
                # check for normal remove lines
                if re.search(r'# remove ....-..-..$', line):
                    expire_date = line.replace('# remove ', '')
                # check for mis-formated remove lines
                elif re.search(r'# remove ../../....$', line):
                    date_parts = line.replace('# remove ', '').split('/')
                    expire_date = '{}-{}-{}'.format(
                        date_parts[2],
                        date_parts[0],
                        date_parts[1],
                    )
                    line = '# remove {}'.format(expire_date)
                # check for never remove
                elif re.search('^# remove never', line):
                    expire_date = False
                header.append(line)

        if expire_date is None:
            print('\nInvalid Entry!\n')
            print('\n'.join(e))

        if not start:
            print('Invalid Entry!')
            print(e)

        return output, removed

    def process_header(self, lines):
        """Process the header from a config file."""
        output = []

        comment = False
        first = True

        indent = 0
        for line in lines:

            if re.search(r'(#|)</', line):
                indent -= 2

            if re.search(r'^#', line):

                if not comment and not first:
                    output.append('')

                comment = True
                if line == '#':
                    output.append(line)
                else:
                    output.append('# {}{}'.format(
                        ' ' * indent,
                        line[1:].strip()
                    ))

            elif re.search(r'^<', line):
                comment = False
                output.append('{}{}'.format(
                    ' '*indent,
                    line
                ))

            else:
                comment = False
                e = line.split()
                if len(e) > 1:
                    output.append('{}{}'.format(
                        ' '*indent+e[0].ljust(32-indent),
                        ' '.join(e[1:]),
                    ))
                elif e:
                    output.append('{}{}'.format(' ' * indent, line))

            if re.search(r'(#|)<[^/]', line):
                indent += 2

            if first:
                first = False

        return output

    def process_inactive(self, e):
        """Process inactive entries."""
        output = ['']
        comment = False
        indent = 0
        for line in e:

            line = line[1:].strip()

            # check if this line is a comment
            if re.search('^ *#', line):
                # check if the previous line was a comment
                if not comment:
                    output.append('#')
                comment = True
            else:
                comment = False

            # check if this line is a close tag
            if re.search(r'^</Anonymous>', line):
                output.append('#')
                indent -= 2
            elif re.search(r'^</Directory>', line):
                indent -= 2
            elif re.search(r'^</Limit>', line):
                indent -= 2

            c = line.split()

            # if this is a comment or a tag, print it as usual
            if re.search("^(#|<)", line):
                output.append('# '+' '*indent + line)

            # if it has more than one word, print it with ljust
            elif len(c) > 1:
                if c[0] in [
                    'AllowAll',
                    'AllowOverwrite',
                    'AnonRequirePassword',
                    'DefaultChdir',
                    'DenyAll',
                    'ExtendedLog',
                    'Group',
                    'MaxClients',
                    'MaxClientsPerHost',
                    'RequireValidShell',
                    'ShowSymlinks',
                    'TransferLog',
                    'User',
                    'UserAlias',
                    'UserPassword',
                ]:
                    output.append('# ' + ' '*indent + c[0].ljust(24) + ' '.join(c[1:]))
                else:
                    output.append('# '+' '*indent + line)

            # if it is just a single word (AllowAll, DenyAll), print it out
            elif c:
                output.append('# '+' '*indent + line)

            # else ignore empty lines

            # check if this line is an open tag
            if re.search(r'^<Limit ', line):
                indent += 2
            elif re.search(r'^<Directory ', line):
                indent += 2
            elif re.search(r'^<Anonymous ', line):
                indent += 2

        return output

    def root_stats(self, active):
        """Get root stats."""
        roots = {}
        for a in active:
            r = a.split('/')[1]
            if r in roots:
                roots[r] += 1
            else:
                roots[r] = 1
        for r in sorted(roots, key=lambda x: roots[x], reverse=True):
            print('   * /{} {}'.format(r, roots[r]))