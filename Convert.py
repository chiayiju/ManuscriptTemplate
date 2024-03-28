import fnmatch;
import os;
import math;
import progressbar;
import sys;

os.system("clear");

files = [];
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*(Track).tex'):
        files.append(file);

if files == []:
    print("No \"(Track)\" file found.\n");
    sys.exit();
else:
    print("Which files to convert?\n");
    for i in range(len(files)):
        print("[", i + 1, "]", files[i]);

    inp = input("\nInput the # of file to be converted (for multiple files, separate them with space or type \"q\" to exit): ").split();
    print();
    if (inp == [] or inp[0].lower() == 'q'):
        print("Abort\n");
        sys.exit();
    else:
        for i in range(len(inp)):
            if (inp[i].isnumeric() == False):
                print("Cannot reconize the input.\n");
                sys.exit();
            elif (int(inp[i]) < 0 or int(inp[i]) > len(files)):
                print("File # out of range.\n");
                sys.exit();
for i in range(len(inp)):
    print("Converting %s to %s:" % (files[int(inp[i]) - 1], files[int(inp[i]) - 1].replace('(Track).tex','.tex')));

    fileread = open(files[int(inp[i]) - 1], 'r');
    filewrite = open(files[int(inp[i]) - 1].replace('(Track).tex','(FullTrack).tex'), 'w');

    def RemoveDoubleSpaces(line):
        ret = '';
        spaces = 0;
        for i in line:
            if i == ' ':
                if spaces == 0:
                    ret += i;
                    spaces += 1;
                else:
                    spaces += 1;
            else:
                ret += i;
                spaces = 0;
        return ret;

    def RemoveEmptyTabs(line):
        ret = line;
        if ret.isspace() == True:
            ret = '\n';
        return ret;

    def RemoveParenthese(line, m, n):
        ret = '';
        skip = 0;
        loops = 0;
        for i in line:
            if loops < m:
                if i == '{':
                    skip += 1;
                elif i == '}' and skip > 0:
                    skip -= 1;
                    if skip == 0:
                        loops += 1;
                elif skip == 0:
                    ret += i;
            elif loops < m + n:
                if i == '{':
                    if skip > 0:
                        ret += i;
                    skip += 1;
                elif i == '}':
                    skip -= 1;
                    if skip == 0:
                        loops += 1;
                    else:
                        ret += i;
                else:
                    ret += i;
            else:
                ret += i;
        return ret;

    def Remove(command, line, m, n):
        i = 0;
        while i < 1:
            i += 1;
            lines = line.split(command, 1);
            temp = '';
            if len(lines) == 2:
                temp = RemoveParenthese(lines[1], m, n);
                line = lines[0] + temp;
                i -= 1;
            else:
                line = lines[0];
        return line;

    def Removing(line):
        global Empty;
        groups = ['fulldalign', 'fullremove'];
        for i in groups:
            if '\\begin{command}'.replace('command', i) in line:
                Empty += 1;
                return '';
            if '\\end{command}'.replace('command', i) in line:
                Empty -= 1;
                return '';
        if Empty > 0:
            return '';
        return line;

    ReadLines = fileread.readlines();
    fileread.close();

    bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]);
    bar.start();

    bar.update(30);

    Empty = 0;
    Lines = [];
    Linetemp = '';
    Inside = False;
    for Line in ReadLines:
        Linetemp = Line;
        
        def RemoveNew(line):
            Run = True;
            if '% For FullTracking' in line:
                Run = False;
            if (Run):
                i = 0;
                while i < 1:
                    i += 1;
                    lines = line.split('\\fulladd{', 1);
                    if len(lines) == 2:
                        temp = '';
                        skip = 1;
                        for j in lines[1]:
                            temp = temp + j;
                            if j == '{':
                                skip += 1;
                            elif j == '}':
                                skip -= 1;
                            if j == '}' and skip == 0:
                                temp = Remove('\\add', temp, 0, 1);
                                temp = Remove('\\delete', temp, 1, 0);
                                temp = Remove('\\replace', temp, 1, 1);
                                temp = Remove('\\mdelete', temp, 1, 0);
                                temp = Remove('\\mreplace', temp, 1, 1);
                                temp = Remove('\\newstart', temp, 0, 0);
                                temp = Remove('\\newend', temp, 0, 0);
                                temp = Remove('\\newpar', temp, 0, 0);
                                temp = Remove('\\nonewpar', temp, 0, 0);
                        line = lines[0] + '\\fulladd{'+ temp;
                    else:
                        line = lines[0];

                    lines = line.split('\\fullreplace{', 1);
                    if len(lines) == 2:
                        temp1 = '';
                        temp2 = '';
                        skip = 1;
                        m = 1;
                        for j in lines[1]:
                            if m == 2:
                                temp2 = temp2 + j;
                                if j == '{':
                                    skip += 1;
                                elif j == '}':
                                    skip -= 1;
                                if j == '}' and skip == 0:
                                    temp2 = Remove('\\add', temp2, 0, 1);
                                    temp2 = Remove('\\delete', temp2, 1, 0);
                                    temp2 = Remove('\\replace', temp2, 1, 1);
                                    temp2 = Remove('\\mdelete', temp2, 1, 0);
                                    temp2 = Remove('\\mreplace', temp2, 1, 1);
                                    temp2 = Remove('\\newstart', temp2, 0, 0);
                                    temp2 = Remove('\\newend', temp2, 0, 0);
                                    temp2 = Remove('\\newpar', temp2, 0, 0);
                                    temp2 = Remove('\\nonewpar', temp2, 0, 0);
                                line = lines[0] + '\\fullreplace{' + temp1 + temp2;
                            else:
                                temp1 = temp1 + j;
                                if j == '{':
                                    skip += 1;
                                elif j == '}':
                                    skip -=1;
                                if j == '}' and skip == 0:
                                    m = 2;
                    else:
                        line = lines[0];

                    lines = line.split('\\fullmreplace{', 1);
                    if len(lines) == 2:
                        temp1 = '';
                        temp2 = '';
                        skip = 1;
                        m = 1;
                        for j in lines[1]:
                            if m == 2:
                                temp2 = temp2 + j;
                                if j == '{':
                                    skip += 1;
                                elif j == '}':
                                    skip -= 1;
                                if j == '}' and skip == 0:
                                    temp2 = Remove('\\add', temp2, 0, 1);
                                    temp2 = Remove('\\delete', temp2, 1, 0);
                                    temp2 = Remove('\\replace', temp2, 1, 1);
                                    temp2 = Remove('\\mdelete', temp2, 1, 0);
                                    temp2 = Remove('\\mreplace', temp2, 1, 1);
                                    temp2 = Remove('\\newstart', temp2, 0, 0);
                                    temp2 = Remove('\\newend', temp2, 0, 0);
                                    temp2 = Remove('\\newpar', temp2, 0, 0);
                                    temp2 = Remove('\\nonewpar', temp2, 0, 0);
                                line = lines[0] + '\\fullmreplace{' + temp1 + temp2;
                            else:
                                temp1 = temp1 + j;
                                if j == '{':
                                    skip += 1;
                                elif j == '}':
                                    skip -=1;
                                if j == '}' and skip == 0:
                                    m = 2;
                    else:
                        line = lines[0];
            return line;

        if '\\fullnewstart' in Linetemp:
            Inside = True;
        if '\\fullnewend' in Linetemp:
            Inside = False;
        if (Inside):
            Linetemp = Remove('\\add', Linetemp, 0, 1);
            Linetemp = Remove('\\delete', Linetemp, 1, 0);
            Linetemp = Remove('\\replace', Linetemp, 1, 1);
            Linetemp = Remove('\\mdelete', Linetemp, 1, 0);
            Linetemp = Remove('\\mreplace', Linetemp, 1, 1);
            Linetemp = Remove('\\newstart', Linetemp, 0, 0);
            Linetemp = Remove('\\newend', Linetemp, 0, 0);
            Linetemp = Remove('\\newpar', Linetemp, 0, 0);
            Linetemp = Remove('\\nonewpar', Linetemp, 0, 0);
            if '\\newstart' in Linetemp:
                Linetemp = '';
            if '\\newend' in Linetemp:
                Linetemp = '';
        else:
            Linetemp = RemoveNew(Linetemp);
            Linetemp = Linetemp.replace('\\usepackage{tracking}', '\\usepackage{fulltracking}');
            Linetemp = Linetemp.replace('\\add', '\\fulladd');
            Linetemp = Linetemp.replace('\\delete', '\\fulldelete');
            Linetemp = Linetemp.replace('\\replace', '\\fullreplace');
            Linetemp = Linetemp.replace('\\mdelete', '\\fullmdelete');
            Linetemp = Linetemp.replace('\\mreplace', '\\fullmreplace');
            Linetemp = Linetemp.replace('\\newadd', '\\fullnewadd');
            Linetemp = Linetemp.replace('\\newstart', '\\fullnewstart');
            Linetemp = Linetemp.replace('\\newend', '\\fullnewend');
            Linetemp = Linetemp.replace('\\newpar', '\\fullnewpar');
            Linetemp = Linetemp.replace('\\nonewpar', '\\fullnonewpar');
            Linetemp = Linetemp.replace('\\begin{remove}', '\\begin{fullremove}');
            Linetemp = Linetemp.replace('\\end{remove}', '\\end{fullremove}');
        if ("".join(Linetemp.split()) != "") and (all(c in '&\\' for c in "".join(Linetemp.split()))):
            Linetemp = "";
        Linetemp = RemoveEmptyTabs(Linetemp);
        Lines.append(RemoveDoubleSpaces(Linetemp));

    LineNum = 0;
    for Line in Lines:
        if (Line == '\n' or Line == '') and (Lines[LineNum - 1] == '\n' or Lines[LineNum - 1] == ''):
            Line = '';
        filewrite.writelines(Line);
        LineNum += 1;

    filewrite.close();

    fileread = open(files[int(inp[i]) - 1].replace('(Track).tex','(FullTrack).tex'), 'r');
    filewrite = open(files[int(inp[i]) - 1].replace('(Track).tex','.tex'), 'w');
    ReadLines = fileread.readlines();
    fileread.close();

    bar.update(60);

    Empty = 0;
    Lines = [];
    Linetemp = '';
    for Line in ReadLines:
        Linetemp = Line;
        Linetemp = Removing(Linetemp);
        Linetemp = Linetemp.replace('\\usepackage{fulltracking}', '');
        #Remove('command', Line, Number of Removes, Number or Keeps)
        Linetemp = Remove('\\fulladd', Linetemp, 0, 1);
        Linetemp = Remove('\\fulldelete', Linetemp, 1, 0);
        Linetemp = Remove('\\fullreplace', Linetemp, 1, 1);
        Linetemp = Remove('\\fullmdelete', Linetemp, 1, 0);
        Linetemp = Remove('\\fullmreplace', Linetemp, 1, 1);
        Linetemp = Remove('\\fullnewstart', Linetemp, 0, 0);
        Linetemp = Remove('\\fullnewend', Linetemp, 0, 0);
        Linetemp = Remove('\\fullnewpar', Linetemp, 0, 0);
        Linetemp = Remove('\\fullnonewpar', Linetemp, 0, 0);
        if ("".join(Linetemp.split()) != "") and (all(c in '&\\' for c in "".join(Linetemp.split()))):
            Linetemp = "";
        Linetemp = RemoveEmptyTabs(Linetemp);
        Lines.append(RemoveDoubleSpaces(Linetemp));

    LineNum = 0;
    for Line in Lines:
        if (Line == '\n' or Line == '') and (Lines[LineNum - 1] == '\n' or Lines[LineNum - 1] == ''):
            Line = '';
        filewrite.writelines(Line);
        LineNum += 1;

    filewrite.close();

    bar.update(100);
    bar.finish();
    print();
print("Done!\n");
