"""Core dataProcessing."""

import re


def get_attributes_from_textfile_process1(text_file):
    """Extract attribute from textfile."""
    with open(text_file, 'rt') as filename:
        lines = filename.readlines()
        for line in lines:
            if 'NAME OF ATTORNEY:' in line:
                name = line.split(':')[-1].replace('|', '').strip()
            if 'TITLE OF PROGRAM: ' in line:
                program = line.split(':')[-1].replace('|', '').replace('_', '').strip()
            if 'DATE(S) OF ATTENDANCE: (For self-study programs, indicate date attorney completed program.)' in line:
                date = line.split(' ')[-1].replace('|', '').strip()
            if 'Ethics and Professionalism' in line and 'Moderator' in line and 'Law competition faculty':
                attendence_ethics_and_professionalism = line.split('|')[0].strip()
                moderator = 'YES' if '[' in line.split('|')[2] or ']' in line.split('|')[2] else 'No'
                law_competition_faculty = 'YES' if '[' in line.split('|')[3] or ']' in line.split('|')[3] else 'NO'
            if 'Skills Enter number of credits earned in each category:\n' in line:
                skills_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                attendence_skill = skills_list[0] if skills_list else None
            if 'Areas of Professional Practice Ethics and Professionalism' in line:
                attendence_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if attendence_list:
                    attendence_area_of_practice = attendence_list[0]
                    if len(attendence_list) > 1:
                        faculty_ethics_professionalism = attendence_list[1]
                else:
                    attendence_area_of_practice = None
                    faculty_ethics_professionalism = None
            if 'Skills\n' in line:
                skills_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                faculty_skills = skills_list[0] if skills_list else None
            if 'Areas of Professional Practice\n' in line:
                area_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                faculty_area_of_pratice = area_list[0] if area_list else None
            i = 0
            if 'Law Practice Management\n' in line:
                if i == 0:
                    law_practice_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                    if law_practice_list: attendence_law_practice = law_practice_list[0]
                if i == 1:
                    law_practice_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                    if law_practice_list: faculty_law_practice = law_practice_list[0]
                i += 1
            else:
                attendence_law_practice = None
                faculty_law_practice = None
            if 'PROVIDER ' in line:
                provider = line.split('|')[1].replace('(check only one)', '')

    return {'name': name, 'title': program, 'date': date,
            'attendance': {'ethics_and_professionalism': attendence_ethics_and_professionalism,
                           'skills': attendence_skill, 'area_of_professional_practice': attendence_area_of_practice,
                           'law_practice_management': attendence_law_practice
                           },
            'faculty': {'ethics_and_professionalism': faculty_ethics_professionalism,
                        'skills': faculty_skills, 'area_of_professional_practice': faculty_area_of_pratice,
                        'law_practice_management': faculty_law_practice
                        },
            'organization': provider}


def get_attributes_from_textfile_process2(text_file):
    """Extract attribute from textfile. pdf - 1346563CLE-NY219141_100266.pdf, 1346563CLE-NY251620_251619_786259.pdf"""

    with open(text_file, 'rt') as filename:
        lines = filename.readlines()
        temp_lines = lines
        for index, line in enumerate(lines):
            if 'Name of Attorney' in line:
                name = lines[index - 1].strip()
            if 'Title of Program' in line:
                title_program = lines[index - 3].strip() + ' ' + lines[index - 2].strip()
            if 'Date(s) of Attendanc' in line:
                date = lines[index - 2].strip()
            if 'Provider Organization' in line:
                provider = lines[index - 2].strip()
            if line == 'E. Credit for Attendance\n': attendence_index = index; print(attendence_index)
            if line == 'In accordance with §10(B)(2) of the Regulations, for multiple breakout sessions,\n': attendance_last_index = index; print(attendance_last_index)

            if line == 'F. Credit for Faculty Participation\n': faculty_index = index; print(faculty_index)
            if line == 'G. CLE Provider Information\n': faculty_last_index = index; print(faculty_last_index)

        for line in temp_lines[attendence_index:attendance_last_index]:
            if 'Ethics and Professionalism\n' in line:
                ethics_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if ethics_list:
                    attendance_ethics_and_professionalism = ethics_list[0]
                else:
                    attendance_ethics_and_professionalism = None
            if 'Skills\n' in line:
                skill_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if skill_list:
                    attendance_skills = skill_list[0]
                else:
                    attendance_skills = None
            if 'Law Practice Management' in line:
                law_practice_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if law_practice_list:
                    attendance_law = law_practice_list[0]
                else:
                    attendance_law = None

            if 'Areas of Professional Practice' in line:
                professional_pra_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if professional_pra_list:
                    attendance_professional_pratice = professional_pra_list[0]
                else:
                    attendance_professional_pratice = None

        for line in temp_lines[faculty_index:faculty_last_index]:
            if 'Ethics and Professionalism\n' in line:
                ethics_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if ethics_list:
                    faculty_ethics_and_professionalism = ethics_list[0]
                else:
                    faculty_ethics_and_professionalism = None

            if 'Skills\n' in line:
                skill_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if skill_list:
                    faculty_skills = skill_list[0]
                else:
                    faculty_skills = None

            if 'Law Practice Management' in line:
                law_practice_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if law_practice_list:
                    faculty_law = law_practice_list[0]
                else:
                    faculty_law = None

            if 'Areas of Professional Practice' in line:
                professional_pra_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if professional_pra_list:
                    faculty_professional_pratice = professional_pra_list[0]
                else:
                    faculty_professional_pratice = None

    return {'name': name, 'title': title_program, 'date': date,
            'attendance': {'ethics_and_professionalism': attendance_ethics_and_professionalism,
                           'skills': attendance_skills, 'area_of_professional_practice': attendance_law,
                           'law_practice_management': attendance_professional_pratice
                           },
            'faculty': {'ethics_and_professionalism': faculty_ethics_and_professionalism,
                        'skills': faculty_skills, 'area_of_professional_practice': faculty_law,
                        'law_practice_management': faculty_professional_pratice
                        },
            'organization': provider}


def get_attributes_from_textfile_process3(text_file):
    """Extract attribute from text_file."""

    with open(text_file, 'rt') as filename:
        lines = filename.readlines()
        for index, line in enumerate(lines):
            if 'NAME OF ATTORNEY:' in line:
                name = line.split(':')[-1].strip()
            if 'TITLE OF PROGRAM:' in line:
                title = line.split(':')[-1].strip()
            if 'DATE(S) OF ATTENDANCE:' in line:
                date = line.split(' ')[-1]
            if 'THE CLE PROVIDER' in line:
                provider = lines[index + 1].replace('(check only one):', '').strip()
            if 'Ethics and Professionalism' in line:
                if 'Areas of Professional Practice' in line:
                    split = line.split('[')
                    if split:
                        split_1list = re.findall(r'[-+]?\d*\.\d+|\d+', split[0])
                        attendance_professional_pratice = split_1list[0] if split_1list else None
                        print('attendance_professional_pratice', attendance_professional_pratice)
                        split_2list = re.findall(r'[-+]?\d*\.\d+|\d+', split[1])
                        faculty_ethics_and_professionalism = split_2list[0] if split_2list else None
                        print('faculty_ethics_and_professionalism', faculty_ethics_and_professionalism)
                if 'Ethics and Professionalism\n' in line:
                    ethics_list = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                    if ethics_list:
                        attendance_ethics_and_professionalism = ethics_list[0]
                    else:
                        attendance_ethics_and_professionalism = None
                    print(attendance_ethics_and_professionalism)
            if 'Skills\n' in line:
                skills = line.split('[')
                if skills:
                    skill_list = re.findall(r'[-+]?\d*\.\d+|\d+', line[-1])
                    if skill_list:
                        faculty_skills = skill_list[0]
                    else:
                        faculty_skills = None

                    if 'Law Practice Management' in skills[0]:
                        law_practice = re.findall(r'[-+]?\d*\.\d+|\d+', skills[0])
                        if law_practice:
                            attendance_law = law_practice[0]
                        else:
                            attendance_law = None
                # print('faculty_skills', faculty_skills)
                # print('attendance_law', attendance_law)
            if 'Law Practice Management\n' in line:
                faculty_laws = line.split('[')
                law_list = re.findall(r'[-+]?\d*\.\d+|\d+', faculty_laws[-1])
                if law_list:
                    faculty_professional_pratice = law_list[0]
                else:
                    faculty_professional_pratice = None
                print('faculty_law', faculty_professional_pratice)
                print('line', line)

            if 'Areas of Professional Practice\n' in line:
                area = line.split('[')
                area_list = re.findall(r'[-+]?\d*\.\d+|\d+', area[-1])
                if area_list:
                    faculty_law = area_list[0]
                else:
                    faculty_law = None

    return {'name': name, 'title': title, 'date': date,
            'attendance': {'ethics_and_professionalism': attendance_ethics_and_professionalism,
                           'skills': None, 'area_of_professional_practice': attendance_law,
                           'law_practice_management': attendance_professional_pratice
                           },
            'faculty': {'ethics_and_professionalism': faculty_ethics_and_professionalism,
                        'skills': faculty_skills, 'area_of_professional_practice': faculty_law,
                        'law_practice_management': faculty_professional_pratice
                        },
            'organization': provider}
