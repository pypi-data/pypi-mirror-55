# !/usr/bin/python 
# coding:utf-8 
import pandas as pd
from classes import MyDataset
import torch
from function import create_mini_batch
from function import get_predictions
from transformers import BertTokenizer
from torch.utils.data import DataLoader
from sklearn.preprocessing import LabelEncoder



        
def output_result(path):
        pd.set_option('chained_assignment',None)
        # Try and catch exception : return 'fail'
        df = pd.read_excel(path)
        old_df = pd.read_excel('RR2016_A8a_A32a.xlsx')
        occ_train = pd.read_csv('occu_train.tsv',sep='\t')
        df_ind = df[['a08a01','k_a08a_1','k_a08a_2','k_a08a_3']]
        df_occ = df[['a08a02','k_a08a_1','k_a08a_2','k_a08a_3','k_a08a_4','k_a08a_5']]
        df_ind.loc[:,'label'] = df_ind.loc[:,'a08a01']
        df_ind.loc[:,'text'] =  df_ind.loc[:,'k_a08a_1'] + '。'+ df_ind.loc[:,'k_a08a_2'] + '。' + df_ind.loc[:,'k_a08a_3']
        df_occ.loc[:,'label'] = df_occ.loc[:,'a08a02']
        df_occ.loc[:,'text'] = df_occ.loc[:,'k_a08a_1'] + '。'+ df_occ.loc[:,'k_a08a_2'] + '。' + df_occ.loc[:,'k_a08a_3'] + '。' + df_occ.loc[:,'k_a08a_4']+ '。' + df_occ.loc[:,'k_a08a_5']
        df_ind = df_ind[['label','text']]
        df_occ = df_occ[['label','text']]

        #要補上Label Encodeing程式碼
        ind_le = LabelEncoder()
        ind_le.fit(old_df['a08a01'])
        #df_ind['label'] = ind_le.transform(df_ind['label'])

        occ_le = LabelEncoder()
        occ_le.fit(occ_train['label'])
        #occ_le['label'] = occ_le.transform(df_occ['label'])

        df_ind.to_csv('ind.tsv',index=0,sep='\t')
        df_occ.to_csv('occ.tsv', index=0, sep='\t')
        ind_tsv = pd.read_csv('ind.tsv',sep = '\t',engine="python")
        occ_tsv = pd.read_csv('occ.tsv', sep='\t', engine="python")
        #occ_tsv = df_occ.to_csv(os.getcwd() + 'occ.tsv',index=0,sep='\t')
        
        PRETRAINED_MODEL_NAME = "bert-base-chinese"  # 指定繁簡中文 BERT-BASE 預訓練模型

        # 取得此預訓練模型所使用的 tokenizer
        tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)
        
        ind_dataset = MyDataset(ind_tsv, tokenizer=tokenizer)
        occ_dataset = MyDataset(occ_tsv, tokenizer=tokenizer)

        BATCH_SIZE = len(df_ind)

        ind_dataloader = DataLoader(ind_dataset, batch_size=BATCH_SIZE, 
                        collate_fn=create_mini_batch)
        occ_dataloader = DataLoader(occ_dataset, batch_size=BATCH_SIZE,
                        collate_fn=create_mini_batch)
        
        #Load model
        ind_model_path = "ind_model.pkl"
        occ_model_path = "occu_model.pkl"
        device = torch.device('cpu')
        ind_model = torch.load(ind_model_path,map_location=device)
        ind_model.eval()
        occ_model = torch.load(occ_model_path,map_location=device)
        occ_model.eval()


        ind_predictions = get_predictions(ind_model, ind_dataloader)
        occ_predictions = get_predictions(occ_model,occ_dataloader)

        # 用Label Encoder Inverse 回去
        ind_pred = ind_le.inverse_transform(ind_predictions)
        occ_pred = occ_le.inverse_transform(occ_predictions)

        ind_pred_df = pd.DataFrame({"ind_predicted": ind_pred.tolist()})
        occ_pred_df = pd.DataFrame({"occ_predicted": occ_pred.tolist()})
        #result_df = pd.concat([df, ind_pred_df.loc[:, 'ind_predicted']], axis=1)
        result_df = pd.concat([df, ind_pred_df.loc[:, 'ind_predicted'],occ_pred_df.loc[:, 'occ_predicted']], axis=1)

        result_df.to_csv('result_file.csv',index=0,encoding = 'utf_8_sig')
        
        return 'success'
        

        




