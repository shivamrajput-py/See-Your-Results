countedview = 0
WEBONSERVER = True

grdpoint = {
    'O':10, 'A+':9, 'A':8, 'B+':7, 'B':6, 'C':5, 'P':4,'F': 0}

shortf_branch26 = {
    'CO': 'Computer Science',
    'IT': 'Information Technology',
    'SE': 'Software Engineering',
    'MC': 'Mathematics and Computing',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'EP': 'Engineering Physics',
    'ME': 'Mechanical Engineering',
    'AE': 'Automotive Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'EN': 'Environmental Engineering',
    'BT': 'Bio-Technology'
}

shortf_branch26REV = dict((v,k) for k,v in shortf_branch26.items())

shortf_branch27 = {
    'CS': 'Computer Science',
    'IT': 'Information Technology',
    'SE': 'Software Engineering',
    'MC': 'Mathematics and Computing',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'EP': 'Engineering Physics',
    'ME': 'Mechanical Engineering',
    'AE': 'Automotive Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'EN': 'Environmental Engineering',
    'BT': 'Bio-Technology'
}

shortf_branch27REV = dict((v,k) for k,v in shortf_branch27.items())

placem_branch_name = {
    'EP': 'Engineering Physics',
    'AE': 'Mechanical Engineering with Specialization in Automotive',
    'CS': 'Computer Engineering',
    'IT': 'Information Technology',
    'MC': 'Mathematics and Computing',
    'CO': 'Computer Engineering',
    'SE': 'Software Engineering',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'BT': 'Bio-Technology',
    'EN': 'Environmental Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Polymer Science and Chemical Technology',
    'PE': 'Production and Industrial Engineering',
    'ME': 'Mechanical Engineering'
}
# 0–30%: early stage / needs boost
cat_0_30 = [
    '<h6 style="font-weight: bold;">🔷 You have outperformed only <span style="color: #87CEFA;">__X__%</span> of your __TYPE__ students — let’s turn this around</h6>',
    '<h6 style="font-weight: bold;">🔷 Currently ranked above only <span style="color: #87CEFA;">__X__%</span> of peers, __TYPE__-wide — time to improve!</h6>',
    '<h6 style="font-weight: bold;">🔷 Only <span style="color: #87CEFA;">__X__%</span> of students scored below you, __TYPE__-wide — let’s aim higher!</h6>',
    '<h6 style="font-weight: bold;">🔷 Your score places you ahead of <span style="color: #87CEFA;">__X__%</span> of peers in the __TYPE__ — keep pushing!</h6>'
]

# 30–50%: making progress
cat_30_50 = [
    '<h6 style="font-weight: bold;">🔷 You’re ahead of <span style="color: #87CEFA;">__X__%</span> of students __TYPE__-wide — steady progress!</h6>',
    '<h6 style="font-weight: bold;">🔷 You outperformed <span style="color: #87CEFA;">__X__%</span> of your peers in the __TYPE__ — keep it up!</h6>',
    '<h6 style="font-weight: bold;">🔷 Above-average: you’ve surpassed <span style="color: #87CEFA;">__X__%</span> of fellow students __TYPE__-wide!</h6>',
    '<h6 style="font-weight: bold;">🔷 Your standing beats <span style="color: #87CEFA;">__X__%</span> of classmates in the __TYPE__ — nice work!</h6>'
]

# 50–70%: above average
cat_50_70 = [
    '<h6 style="font-weight: bold;">🔷 Great work! You’re within the top <span style="color: #87CEFA;">__X__%</span> of the __TYPE__.</h6>',
    '<h6 style="font-weight: bold;">🔷 Your result places you in the top <span style="color: #87CEFA;">__X__%</span> __TYPE__-wide, Damn.</h6>',
    '<h6 style="font-weight: bold;">🔷 Impressive effort: you’re in the top <span style="color: #87CEFA;">__X__%</span> of the __TYPE__!</h6>',
]

# 70–100%: high achievers
cat_70_100 = [
    '<h6 style="font-weight: bold;">🔷 Outstanding! You rank in the top <span style="color: #87CEFA;">__X__%</span> of the __TYPE__.</h6>',
    '<h6 style="font-weight: bold;">🔷 Elite status: you’re among the top <span style="color: #87CEFA;">__X__%</span> of students __TYPE__-wide!</h6>',
    '<h6 style="font-weight: bold;">🔷 Phenomenal! Only <span style="color: #87CEFA;">__X__%</span> of peers in the __TYPE__ match your performance.</h6>',
    '<h6 style="font-weight: bold;">🔷 You’ve secured a spot in the top <span style="color: #87CEFA;">__X__%</span> of peers in the __TYPE__, Excellent!</h6>'
]

# Combined list of all categories
tile_sentences = [cat_0_30, cat_30_50, cat_50_70, cat_70_100]