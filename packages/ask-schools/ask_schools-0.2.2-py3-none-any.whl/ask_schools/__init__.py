__version__ = '0.2.2'

school_name = {
    'Toronto':{'suffix':'_tor', 'short':'Toronto', 'full':'University of Toronto'},
    'Mentee':{'suffix':'_int', 'short':'Mentee', 'full':'Mentee'},
    'Western':{'suffix':'_west', 'short':'Western', 'full':'University of Western Ontario'},
    'Carleton':{'suffix':'_car', 'short':'Carleton', 'full':'Carleton University'},
    'Ryerson':{'suffix':'_rye', 'short':'Ryerson', 'full':'Ryerson University'},
    'Laurentian':{'suffix':'_lan', 'short':'Laurentian', 'full':'Laurentian University'},
    'Queens':{'suffix':'_queens', 'short':'Queens', 'full':'Queens university'},
    'Brock':{'suffix':'_brk', 'short':'Brock', 'full':'Brock University'},
    'Guelph-Humber':{'suffix':'_guehum', 'short':'Guelph-Humber', 'full':'University of Guelph-Humber'},
    'Guelph':{'suffix':'_gue', 'short':'Guelph', 'full':'University of Guelph'},
    'Ontario Tech':{'suffix':'_uoit', 'short':'Ontario Tech', 'full':'Ontario Tech University'},
    'Ontario Tech':{'suffix':'_otech', 'short':'Ontario Tech', 'full':'Ontario Tech University'},
    'Saint-Paul':{'suffix':'_stp', 'short':'Saint-Paul', 'full':'Saint-Paul University'},
    'OCAD':{'suffix':'_ocad', 'short':'OCAD', 'full':'OCAD'},
    'Lakehead':{'suffix':'_lake', 'short':'Lakehead', 'full':'Lakehead university'},
    'Algoma':{'suffix':'_alg', 'short':'Algoma', 'full':'Algoma university'},
    'McMaster':{'suffix':'_mac', 'short':'McMaster', 'full':'McMaster university'},
    'York':{'suffix':'_york', 'short':'York', 'full':'York university'},
    'Scholars Portal':{'suffix':'_sp', 'short':'Scholars Portal', 'full':'Scholars Portal'},
    'Ottawa':{'suffix':'_ott', 'short':'Ottawa', 'full':'Ottawa University'}
}

def find_schools_by_mentee_suffix(operator: str) -> str:
    """from a suffix find the short name of that School
    
    Arguments:
        operator {str} -- suffix of the schoo i.e. _tor
    
    Returns:
        str -- The short name of the school i.e. Toronto
    """
    if "_tor" in operator:
        return "Toronto"
    elif "_int" in operator:
        return "Mentee"
    elif "_west" in operator:
        return "Western"
    elif "_car" in operator:
        return "Carleton"
    elif "_rye" in operator:
        return "Ryerson"
    elif "_lan" in operator:
        return "Laurentian"
    elif "_queens" in operator:
        return "Queens"
    elif "_brk" in operator:
        return "Brock"
    elif "_guehum" in operator:
        return "Guelph-Humber"
    elif "_gue" in operator:
        return "Guelph"
    elif "_uoit" in operator:
        return "Ontario Tech"
    elif "_otech" in operator:
        return "Ontario Tech"
    elif "_stp" in operator:
        return "Saint-Paul"
    elif "_ocad" in operator:
        return "OCAD"
    elif "_lake" in operator:
        return "Lakehead"
    elif "_alg" in operator:
        return "Algoma"
    elif "_mac" in operator:
        return "McMaster"
    elif "_york" in operator:
        if ".fr" in operator:
            return "York-Glendon"
        else:
            return "York"
    elif "_sp" in operator:
        return "Scholars Portal"
    elif "_ott" in operator:
        return "Ottawa"
    else:
        return "Unknown"


if __name__ == '__main__':
    pass