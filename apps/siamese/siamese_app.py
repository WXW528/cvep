#
import os
import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
from torch.autograd import Variable
import PIL.ImageOps    
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
#
from apps.siamese.siamese_config import SiameseConfig
from apps.siamese.atnt_face_ds import AtntFaceDs
from apps.siamese.siamese_network import SiameseNetwork
from apps.siamese.contrastive_loss import ContrastiveLoss

class SiameseApp(object):
    def __init__(self):
        self.refl = 'apps.siamese.SiameseApp'
        self.pkl_file = './work/siamese/siamese.pkl'

    def startup(self, args={}):
        print('Siamese Network App v0.0.2')
        os.environ['CUDA_VISIBLE_DEVICES'] = '3' # ','.join(map(str, [2]))
        self.train()
        self.run()

    def train(self):
        folder_dataset = dset.ImageFolder(root=SiameseConfig.training_dir)
        siamese_dataset = AtntFaceDs(imageFolderDataset=folder_dataset,
                                        transform=transforms.Compose([transforms.Resize((SiameseConfig.img_w, SiameseConfig.img_h)),
                                                                      transforms.ToTensor()
                                                                      ])
                                       ,should_invert=False)
        train_dataloader = DataLoader(siamese_dataset,
                        shuffle=True,
                        num_workers=8,
                        batch_size=SiameseConfig.train_batch_size)
        net = SiameseNetwork().cuda()
        criterion = ContrastiveLoss()
        optimizer = optim.Adam(net.parameters(),lr = 0.0005 )
        counter = []
        loss_history = [] 
        iteration_number= 0
        for epoch in range(0, SiameseConfig.train_number_epochs):
            epoch_loss = 0
            epoch_num = 0
            for i, data in enumerate(train_dataloader,0):
                img0, img1 , label = data
                img0, img1 , label = Variable(img0).cuda(), Variable(img1).cuda() , Variable(label).cuda()
                output1,output2 = net(img0,img1)
                optimizer.zero_grad()
                loss_contrastive = criterion(output1,output2,label)
                loss_contrastive.backward()
                optimizer.step()
                batch_loss = loss_contrastive.data.item()
                epoch_loss += batch_loss
                epoch_num += 1
                if i %10 == 0 :
                    #print("Epoch{}: {} Current loss {}".format(epoch, i, loss_contrastive.data.item()))
                    iteration_number +=10
                    counter.append(iteration_number)
                    loss_history.append(batch_loss)
            print("Epoch{}: Current loss {}".format(epoch, epoch_loss / epoch_num))
        self.show_plot(counter,loss_history)
        torch.save(net.state_dict(), self.pkl_file)

    def run(self):
        net = SiameseNetwork()
        net.load_state_dict(torch.load(self.pkl_file))
        net.cuda()
        folder_dataset_test = dset.ImageFolder(root=SiameseConfig.testing_dir)
        siamese_dataset = AtntFaceDs(imageFolderDataset=folder_dataset_test,
                                        transform=transforms.Compose([transforms.Resize((SiameseConfig.img_w, SiameseConfig.img_h)),
                                                                      transforms.ToTensor()
                                                                      ])
                                       ,should_invert=False)
        test_dataloader = DataLoader(siamese_dataset,num_workers=6,batch_size=1,shuffle=True)
        dataiter = iter(test_dataloader)
        x0, _, _ = next(dataiter)
        for i in range(10):
            _,x1,label2 = next(dataiter)
            concatenated = torch.cat((x0,x1),0)            
            output1,output2 = net(Variable(x0).cuda(), Variable(x1).cuda())
            distance = F.pairwise_distance(output1, output2)
            #distance = 1 - F.cosine_similarity(output1, output2)
            img_file = './logs/img_{0:03d}'.format(i)
            self.imshow(torchvision.utils.make_grid(concatenated), img_file, 
                        'Dissimilarity:{0:0.2f}'.format(
                            distance.cpu().data.numpy()[0]
                        ))
            print('concatenated: {0}; {1};'.format(concatenated.shape, type(concatenated)))
            print('Dissimilarity:{0:0.2f}'.format(
                            distance.cpu().data.numpy()[0]
                        ))











    def ds_demo(self):
        folder_dataset = dset.ImageFolder(root=SiameseConfig.training_dir)
        siamese_dataset = AtntFaceDs(imageFolderDataset=folder_dataset,
                                        transform=transforms.Compose([transforms.Resize((SiameseConfig.img_w,SiameseConfig.img_h)),
                                                                      transforms.ToTensor()
                                                                      ])
                                       ,should_invert=False)
        vis_dataloader = DataLoader(siamese_dataset,
                        shuffle=True,
                        num_workers=8,
                        batch_size=8)
        dataiter = iter(vis_dataloader)


        example_batch = next(dataiter)
        print('example_batch: {0};'.format(example_batch[0].shape))
        concatenated = torch.cat((example_batch[0],example_batch[1]),0)
        self.imshow(torchvision.utils.make_grid(concatenated))
        print(example_batch[2].numpy())

    def imshow(self, img, img_file, text=None, should_save=False):
        npimg = img.numpy()
        plt.axis("off")
        if text:
            plt.text(75, 8, text, style='italic',fontweight='bold',
                bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        #plt.show()  
        plt.savefig(img_file)  

    def show_plot(self, iteration,loss):
        plt.plot(iteration,loss)
        plt.show()