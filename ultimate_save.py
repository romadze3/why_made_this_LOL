def save_lives(hp):
    with open('hp_sohranenie.txt','w') as f:
        print(hp,file=f)

def load_lives():
    with open('hp_sohranenie.txt','r') as f:
        a = f.read()
        return int(a)


def save(score):
    with open('scores_total.txt','w',encoding='utf-8') as f:
        print(str(score),file = f)

def load_score():
    with open('scores_total.txt','r') as f:
        a = f.read()
        return int(a)