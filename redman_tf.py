import tensorflow as tf
import os
os.chdir('/data/qingyong/Redman')
import numpy as np
import matplotlib.pylab as plt
import time
import pqyMLscore
import scipy.signal as signal

gengdata, gengtarget = pqyMLscore.load_training_data('gengtrainingdataV90.npy')
zhangdata, zhangtarget = pqyMLscore.load_training_data('zhangtrainingdataV90.npy')
goldendata, goldentarget = pqyMLscore.load_training_data('goldentrainingdataV90.npy')


sample_data=np.vstack((gengdata[:,1:],zhangdata[:,1:]))
goldendata=goldendata[:,1:]
temptime=time.time()
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# scaler.fit(sample_data)
# sample_data1 = scaler.transform(sample_data)
sample_data1=sample_data/210
# goldendata1=scaler.transform(goldendata)
goldendata1=goldendata/210
datasizeM,datasizeN=sample_data1.shape
Xhat=signal.medfilt(sample_data1,5)
print('datasizeM:%d,datasizeN%d'%(datasizeM,datasizeN))
print(time.time()-temptime)
m,n=sample_data1.shape
learn_rate=0.0001
train_batch=256
n_input=n

n_hidden1=1000
n_hidden2=800
n_hidden3=600
n_hidden4=400
n_hidden5=300
n_hidden6=200
n_hidden7=100

weights={
    'encoder_h1':tf.Variable(tf.truncated_normal([n_input,n_hidden1])),
    'encoder_h2':tf.Variable(tf.truncated_normal([n_hidden1,n_hidden2])),
    'encoder_h3':tf.Variable(tf.truncated_normal([n_hidden2,n_hidden3])),
    'encoder_h4':tf.Variable(tf.truncated_normal([n_hidden3,n_hidden4])),
    'encoder_h5':tf.Variable(tf.truncated_normal([n_hidden4,n_hidden5])),
    'encoder_h6':tf.Variable(tf.truncated_normal([n_hidden5,n_hidden6])),
    'encoder_h7':tf.Variable(tf.truncated_normal([n_hidden6,n_hidden7])),
    'decoder_h1':tf.Variable(tf.truncated_normal([n_hidden7,n_hidden6])),
    'decoder_h2':tf.Variable(tf.truncated_normal([n_hidden6,n_hidden5])),
    'decoder_h3':tf.Variable(tf.truncated_normal([n_hidden5,n_hidden4])),
    'decoder_h4':tf.Variable(tf.truncated_normal([n_hidden4,n_hidden3])),
    'decoder_h5':tf.Variable(tf.truncated_normal([n_hidden3,n_hidden2])),
    'decoder_h6':tf.Variable(tf.truncated_normal([n_hidden2,n_hidden1])),
    'decoder_h7':tf.Variable(tf.truncated_normal([n_hidden1,n_input]))
}

bise={
    'encoder_h1':tf.Variable(tf.truncated_normal([n_hidden1])),
    'encoder_h2':tf.Variable(tf.truncated_normal([n_hidden2])),
    'encoder_h3':tf.Variable(tf.truncated_normal([n_hidden3])),
    'encoder_h4':tf.Variable(tf.truncated_normal([n_hidden4])),
    'encoder_h5':tf.Variable(tf.truncated_normal([n_hidden5])),
    'encoder_h6':tf.Variable(tf.truncated_normal([n_hidden6])),
    'encoder_h7':tf.Variable(tf.truncated_normal([n_hidden7])),
    'decoder_h1':tf.Variable(tf.truncated_normal([n_hidden6])),
    'decoder_h2':tf.Variable(tf.truncated_normal([n_hidden5])),
    'decoder_h3':tf.Variable(tf.truncated_normal([n_hidden4])),
    'decoder_h4':tf.Variable(tf.truncated_normal([n_hidden3])),
    'decoder_h5':tf.Variable(tf.truncated_normal([n_hidden2])),
    'decoder_h6':tf.Variable(tf.truncated_normal([n_hidden1])),
    'decoder_h7':tf.Variable(tf.truncated_normal([n_input]))
}

def encode(x):
    layer1=tf.nn.sigmoid(tf.add(tf.matmul(x,weights['encoder_h1']),bise['encoder_h1']))
    layer2=tf.nn.sigmoid(tf.add(tf.matmul(layer1,weights['encoder_h2']),bise['encoder_h2']))
    layer3=tf.nn.sigmoid(tf.add(tf.matmul(layer2,weights['encoder_h3']),bise['encoder_h3']))
    layer4=tf.nn.sigmoid(tf.add(tf.matmul(layer3,weights['encoder_h4']),bise['encoder_h4']))
    layer5=tf.nn.sigmoid(tf.add(tf.matmul(layer4,weights['encoder_h5']),bise['encoder_h5']))
    layer6=tf.nn.sigmoid(tf.add(tf.matmul(layer5,weights['encoder_h6']),bise['encoder_h6']))
    layer7=(tf.add(tf.matmul(layer6,weights['encoder_h7']),bise['encoder_h7']))
    return layer7

def decode(x):
    layer1=tf.nn.sigmoid(tf.add(tf.matmul(x,weights['decoder_h1']),bise['decoder_h1']))
    layer2=tf.nn.sigmoid(tf.add(tf.matmul(layer1,weights['decoder_h2']),bise['decoder_h2']))
    layer3=tf.nn.sigmoid(tf.add(tf.matmul(layer2,weights['decoder_h3']),bise['decoder_h3']))
    layer4=tf.nn.sigmoid(tf.add(tf.matmul(layer3,weights['decoder_h4']),bise['decoder_h4']))
    layer5=tf.nn.sigmoid(tf.add(tf.matmul(layer4,weights['decoder_h5']),bise['decoder_h5']))
    layer6=tf.nn.sigmoid(tf.add(tf.matmul(layer5,weights['decoder_h6']),bise['decoder_h6']))
    layer7=(tf.add(tf.matmul(layer6,weights['decoder_h7']),bise['decoder_h7']))
    return layer7

X=tf.placeholder('float',[None,n_input])
encode_out=encode(X)
decode_out=decode(encode_out)

Y=tf.placeholder('float',[None,n_input])
loss=tf.reduce_mean(tf.pow(Y-decode_out,2))
optimizer=tf.train.AdamOptimizer(learn_rate).minimize(loss)
print('网络已创建')
training_epochs = 1000
display_step = 1
sess=tf.Session()
init=tf.initialize_all_variables()
sess.run(init)
total_batch = int(m/train_batch)
for epoch in range(training_epochs):
    for i in range(total_batch):
        _, c = sess.run([optimizer, loss], feed_dict={X: sample_data1[i:i+train_batch,:],Y: Xhat[i:i+train_batch,:]})
    if epoch % display_step == 0:
        print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c))
    if c<=0.0001:
        break
print("Optimization Finished!")

num=7777
dataout=sess.run(decode_out,feed_dict={X: sample_data1[num,:].reshape(1,-1)})
plt.figure(figsize=(20,10))
plt.plot(signal.medfilt(sample_data1[num,:],5))
plt.plot(dataout.flatten())
plt.ylim(0,1)
plt.show()