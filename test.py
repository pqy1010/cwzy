import tensorflow as tf
import numpy as np
import time
sample_data1=np.arange(12).reshape((3,4))
m, n = sample_data1.shape
learn_rate = 0.0001
train_batch = 256
n_input = n

# n_hidden1 = 1000
# n_hidden2 = 800
# n_hidden3 = 600
# n_hidden4 = 400
# n_hidden5 = 300
# n_hidden6 = 200
# n_hidden7 = 100

hidden = [n_input,1000,800]
hiddenlen = len(hidden)
weights=dict()
bise=dict()

for i in range(1,len(hidden)):
    # encoder w
    w_this_encoder_str = 'encoder_h%d' % i
    w_lastencoderhidden = hidden[i - 1]
    w_thisencoderhidden = hidden[i]
    weights[w_this_encoder_str] = tf.Variable(tf.truncated_normal([w_lastencoderhidden, w_thisencoderhidden]))
    # decoder w
    w_this_decoder_str = 'decoder_h%d' % i
    w_thisdecoderhidden = hidden[hiddenlen - i - 1]
    w_lasedecoderhidden = hidden[hiddenlen - i]
    weights[w_this_decoder_str] = tf.Variable(tf.truncated_normal([w_lasedecoderhidden, w_thisdecoderhidden]))

    # encoder b
    bise[w_this_encoder_str]=tf.Variable(tf.truncated_normal([hidden[i]]))

    # decoder b

    bise[w_this_decoder_str] = tf.Variable(tf.truncated_normal([hidden[hiddenlen-i-1]]))




def encode(x):
    layer_res=dict()

    for i in range(1,len(hidden)):
        layerstr='layer_%d'%i
        lastlayerstr = 'layer_%d' % (i - 1)
        w_this_encoder_str = 'encoder_h%d' % i
        if i==1:
            layer_res[layerstr] = tf.nn.sigmoid(tf.add(tf.matmul(x, weights[w_this_encoder_str]), bise[w_this_encoder_str]))
        elif i==len(hidden)-1:
            return tf.add(tf.matmul(layer_res[lastlayerstr], weights[w_this_encoder_str]), bise[w_this_encoder_str])
        else:
            layer_res[layerstr] = tf.nn.sigmoid(tf.add(tf.matmul(layer_res[lastlayerstr], weights[w_this_encoder_str]), bise[w_this_encoder_str]))


def decode(x):
    layer_res=dict()

    for i in range(1,len(hidden)):
        layerstr='layer_%d'%i
        lastlayerstr = 'layer_%d' % (i - 1)
        w_this_encoder_str = 'decoder_h%d' % i
        if i==1:
            layer_res[layerstr] = tf.nn.sigmoid(tf.add(tf.matmul(x, weights[w_this_encoder_str]), bise[w_this_encoder_str]))
        elif i==len(hidden)-1:
            return tf.add(tf.matmul(layer_res[lastlayerstr], weights[w_this_encoder_str]), bise[w_this_encoder_str])
        else:
            layer_res[layerstr] = tf.nn.sigmoid(tf.add(tf.matmul(layer_res[lastlayerstr], weights[w_this_encoder_str]), bise[w_this_encoder_str]))

X=tf.placeholder('float',[None,n_input])
encode_out=encode(X)
decode_out=decode(encode_out)

Y=tf.placeholder('float',[None,n_input])
loss=tf.reduce_mean(tf.pow(Y-decode_out,2))
optimizer=tf.train.AdamOptimizer(learn_rate).minimize(loss)
print('网络已创建')
training_epochs = 500000
display_step = 1
sess=tf.Session()
init=tf.global_variables_initializer()
sess.run(init)
total_batch = int(m/train_batch)
for epoch in range(training_epochs):
    for i in range(total_batch):
        _, c = sess.run([optimizer, loss], feed_dict={X: sample_data1[i:i+train_batch,:],Y: Xhat[i:i+train_batch,:]})
    if epoch % display_step == 0:
        print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c))
    if c<=0.000001:
        break
print("Optimization Finished!")



time.sleep(1)