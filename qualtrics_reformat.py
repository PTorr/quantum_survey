from read_data import read_data
import numpy as np
import pandas as pd


def main():
    table_path = 'D:\Users\Torr\PycharmProjects\quantum_survey/emma_survey_5.csv'
    [questions_id, question_answers] = reformat_data(table_path)
    # print np.matrix(questions_id)
    print np.matrix(question_answers)


def reformat_data(table_path):
    # data = read_data(table_path)
    data = pd.read_csv(table_path, header=None)
    dr = len(data)  # number of rows in the data
    dc = len(data.T)  # number of columns (participants) in the data
    q_value = np.ndarray((dc - 2, dr - 17), float)

    qid = data[1][16:dr - 1]  # qid is the question number
    for i in range(len(q_value)):
        qtemp = data[i + 2][16:dr - 1]  # answers/ probabilities
        qtemp = np.asarray(qtemp)
        q_value[i, :] = qtemp
        print i
    qid = qid.tolist()

    qid = np.asarray(qid)

    qid = [q.split('.') for q in qid]
    qid1 = [q[1].split('_') for q in qid]
    qid = [q[0].split('_') for q in qid]

    i = 0
    j = 0
    idx_rmv = []
    for q in qid1:
        if len(q) == 2:
            q = q[1].split(' ')
            try:
                int(q[0])
                dn = 1
            except ValueError:
                dn = 0
            if dn == 1:
                pass
            elif dn == 0:
                if q[0] == 'Page':
                    qid[i] = 'timing_question'
                    pass
                else:
                    idx_rmv.append(i)
                    j += 1
        i += 1

    qid = np.delete(qid, idx_rmv)
    for i in idx_rmv:
        print i
        # q_value = np.delete(q_value, i, axis=0)  # axis=0 means rows

    # q_value = map(int,q_value)

    # ------------------------------------------------------------------------------------------------------------
    # creates dictionary {question:indicies of values}
    # available_qid = np.unique(qid)
    # d = {}
    # for q in available_qid:
    #     indices = [i for i, x in enumerate(qid) if x == available_qid[0]]
    #     indices = map(int, indices)
    #     d[q[0]] = indices
    # a = d['Q1']
    # ------------------------------------------------------------------------------------------------------------

    qid = [q[0] for q in qid]

    # print qid[qid == available_qid[0]]
    # print q_value[qid == available_qid[0]]

    return qid, q_value


if __name__ == '__main__':
    main()
