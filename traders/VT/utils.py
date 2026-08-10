from datetime import datetime
import json

def get_pages(filename:str):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return tuple(data.keys())

def open_configuration_traiders(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def get_configuration_traiders(data,page):
    data = data[page]
    doms = []
    charts = []
    charts = []
    amount = data["amount"]
    pos_offset = data['pos_offset']
    for raw_dom in data['doms']:
        dom = {
            'clusters':[],
            'tapes':[],
            'glasses':[],
            'poses':[]
        }
        dom_field = raw_dom['dom_field_xyxy']
        start_dom = dom_field[0]
        if raw_dom['direction'] == 'column':
            width_dom = dom_field[2]-start_dom
        else:
            width_dom = (dom_field[2]-start_dom)//amount
        end_cluster = raw_dom['f_cluster_e_x'] - start_dom
        start_tape = raw_dom['f_tape_se_xx'][0] - start_dom
        end_tape = raw_dom['f_tape_se_xx'][1] - start_dom
        start_glass = raw_dom['f_glass_s_x'] - start_dom
        end_glass = start_dom + width_dom - 2
        start_pos = start_dom + width_dom//3
        end_pos = start_pos + width_dom//3
        high_dom = dom_field[1]
        if raw_dom['direction'] == 'column':
            heigh_dom = (dom_field[3]-dom_field[1])//amount
            low_dom = dom_field[1] + heigh_dom - pos_offset
            for i in range(amount):
                y1 = high_dom+heigh_dom*i
                y2 = low_dom+heigh_dom*i 
                dom['clusters'].append((start_dom,y1,end_cluster,y2))
                dom['tapes'].append((start_tape,y1,end_tape,y2))
                dom['glasses'].append((start_glass,y1,end_glass,y2))

                dom['poses'].append((start_pos,y2+pos_offset-6,end_pos,y2+pos_offset-1))
        else:
            low_dom = dom_field[3] - pos_offset
            for i in range(amount):
                offset_x1 = width_dom*i
                dom['clusters'].append((start_dom+offset_x1,high_dom,end_cluster+offset_x1,low_dom))
                dom['tapes'].append((start_tape+offset_x1,high_dom,end_tape+offset_x1,low_dom))
                dom['glasses'].append((start_glass+offset_x1,high_dom,end_glass+offset_x1,low_dom))
                dom['poses'].append((start_pos+offset_x1,dom_field[3]-1,end_pos+offset_x1,dom_field[3]-6))
        doms.append(dom)
    for raw_charts in data['charts']:
        field = raw_charts['field']
        line_chart = []
        if raw_charts['direction'] == 'column':
            heigh_chart = (field[3]-field[1])//amount
            for i in range(amount):
                offset = heigh_chart*i
                line_chart.append((field[0],field[1]+offset,field[2],field[1]+offset+heigh_chart))
        else:
            width_chart = (field[2]-field[0])//amount
            for i in range(amount):
                offset = width_chart*i
                line_chart.append((field[0]+offset,field[1],field[0]+offset+width_chart,field[3]))
        charts.append(line_chart)
    conf_data = {
        'doms':doms,
        'charts':charts,
        'price_step':data["price_step"],
        'amount':amount
    }
    return conf_data

def only_close(action,hour,minute):
    now = datetime.now()
    chour = now.hour
    cminute = now.minute
    end_minute = minute + 15
    if hour == chour:
        if end_minute > cminute > minute:
            if action == 'long':
                return 'close_short'
            if action == 'short':
                return 'close_long'
        if end_minute < cminute:
            return 'close_all'
    return action