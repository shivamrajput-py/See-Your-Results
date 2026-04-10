import io
with io.open('1_STUDENT_PROFILE.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('                    st.write(f"""<h3'):
        lines[i] = line[4:]
    elif line.startswith('                    st.write(f"""\n'):
        lines[i] = line[4:]
        
with io.open('1_STUDENT_PROFILE.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
