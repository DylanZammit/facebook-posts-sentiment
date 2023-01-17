import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILE_NAME = 'output.csv'


if __name__=='__main__':
    
    df = pd.read_csv(FILE_NAME, index_col=0)

    if 1:
        df_1 = df[df.sent_label!='unclassified']
        df_1 = df_1[['post_id', 'page_name', 'sent_label']].groupby(['page_name', 'sent_label']).count()
        df_1 = df_1.unstack()
        df_1.columns = [x[1] for x in df_1.columns]
        df_1 = df_1.rename({v: v[0].upper() + v[1:] for v in df_1.columns}, axis=1)

        df_1 = df_1.div(df_1.sum(axis=1), axis=0)
        df_1 = df_1.sort_values('Negative')
        df_1.plot(kind='barh', stacked=True, title='Post Sentiment', mark_right=True, color=['r', 'orange', 'g'])

        df_1 = df_1.sort_values('Positive')
        df_1.plot(kind='barh', stacked=True, title='Post Sentiment', mark_right=True, color=['r', 'orange', 'g'])

    if 1:
        df_2 = df[['page_name', 'num_haha', 'num_love', 'num_like', 'num_angry', 'num_wow', 'num_sad']].groupby('page_name').sum()
        df_2 = df_2.div(df_2.sum(axis=1), axis=0)
        df_2.plot(kind='barh', stacked=True, title='Post Sentiment', mark_right=True)

    if 1:
        plt.figure()
        df_3 = df[(df.sent_label!='unclassified')&(df.sent_label!='neutral')]
        df_3 = df_3[['page_name', 'num_reacts', 'sent_label']].groupby(['page_name', 'sent_label']).sum().unstack()
        df_3 = df_3.div(df_3.sum(axis=1), axis=0)
        df_3.columns = [x[1] for x in df_3.columns]
        df_3 = df_3.sort_values('negative')
        df_3.plot(kind='barh', stacked=True, title='Number of Reacts', mark_right=True)
        print(df_3)

    if 1:
        plt.figure()
        df_3 = df[(df.sent_label!='unclassified')&(df.sent_label!='neutral')]
        df_3 = df_3[['page_name', 'num_comments', 'sent_label']].groupby(['page_name', 'sent_label']).sum().unstack()
        df_3 = df_3.div(df_3.sum(axis=1), axis=0)
        df_3.columns = [x[1] for x in df_3.columns]
        df_3 = df_3.sort_values('negative')
        df_3.plot(kind='barh', stacked=True, title='Number of Comments', mark_right=True)
        print(df_3)

    A = df[df.sent_label.isin(['negative', 'positive'])].sort_values('num_reacts', ascending=True)['sent_label'].reset_index(drop=True)
    B = df[df.sent_label=='positive'].sort_values('num_reacts', ascending=False)[['caption', 'page_name', 'num_reacts']].head(5)
    C = df[df.sent_label=='positive'].sort_values('num_reacts', ascending=False)[['caption', 'page_name', 'num_reacts']].head(5)

    plt.show()
