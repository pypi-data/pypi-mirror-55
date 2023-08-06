import torch
#from torch.utils.data import Dataset
#from transformers import BertTokenizer
#from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence



def create_mini_batch(samples):
        tokens_tensors = [s[0] for s in samples]
        segments_tensors = [s[1] for s in samples]
        
        # 測試集有 labels
        if samples[0][2] is not None:
            label_ids = torch.stack([s[2] for s in samples])
        else:
            label_ids = None
        
        # zero pad 到同一序列長度
        tokens_tensors = pad_sequence(tokens_tensors, 
                                        batch_first=True)
        segments_tensors = pad_sequence(segments_tensors, 
                                            batch_first=True)
            
        # attention masks，將 tokens_tensors 裡頭不為 zero padding
        # 的位置設為 1 讓 BERT 只關注這些位置的 tokens
        masks_tensors = torch.zeros(tokens_tensors.shape, 
                                        dtype=torch.long)
        masks_tensors = masks_tensors.masked_fill(
                tokens_tensors != 0, 1)
            
        return tokens_tensors, segments_tensors, masks_tensors, label_ids

def get_predictions(model, dataloader, compute_acc=False):
        predictions = None
        correct = 0
        total = 0
            
        model.eval()  # 推論模式
        with torch.no_grad():
            # 遍巡整個資料集
            for data in dataloader:
                # 將所有 tensors 移到 GPU 上
                if next(model.parameters()).is_cuda:
                    data = [t.to("cuda:0") for t in data if t is not None]
                    
                outputs = model(*data[:3])
                    
                # 別忘記前 3 個 tensors 分別為 tokens, segments 以及 masks
                logits = outputs[0]
                _, pred = torch.max(logits.data, 1)
                    
                # 用來計算訓練集的分類準確率
                if compute_acc:
                    labels = data[3]
                    total += labels.size(0)
                    correct += (pred == labels).sum().item()
                        
                # 將當前 batch 記錄下來
                if predictions is None:
                    predictions = pred
                else:
                    predictions = torch.cat((predictions, pred))
                    
                break
            
        if compute_acc:
            acc = correct / total
            return predictions, acc
        return predictions
            