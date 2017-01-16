import numpy as np
# from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

# mnist = input_data.read_data_sets('MNIST_data', one_hot=True)








total=0
def next_batch(n):

	global mydata
	global mylabels
	global total


	if (total <= mydata.shape[0]-n):
		z = mydata   [total : total+n,   :]
		y = mylabels [total : total+n,   :]
		total = total + n

	else :

		z = mydata   [0 : 0+n,   :]
		y = mylabels [0 : 0+n,   :]
		total= n



	return (z.astype(np.float32) ,y.astype(np.float32) )



# batch2 = next_batch(50)
# c=batch2[0]
# print c.shape
# x= c[1,1]
# print x.dtype



sess = tf.InteractiveSession()



mydata   = np.random.rand(200,65536)
# mydata   = np.random.rand(200,784)
mylabels = np.random.rand(200,1)



x = tf.placeholder(tf.float32, shape=[None, 65536])
# x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 1])




def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')



def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
# x_image = tf.reshape(x, [-1,28,28,1])
x_image = tf.reshape(x, [-1,256,256,1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_fc1 = weight_variable([64 * 64 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 64*64*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


W_fc2 = weight_variable([1024, 1])
b_fc2 = bias_variable([1])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2


# cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))

msqe = tf.reduce_mean(tf.square(y_conv - y_))


train_step = tf.train.AdamOptimizer(1e-4).minimize(msqe)
# correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())


for i in range(400):
  # batch = mnist.train.next_batch(50)
  batch = next_batch(50)

  if i%100 == 0:
    error = msqe.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training error %g"%(i, error))

  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

# print("test accuracy %g"%accuracy.eval(feed_dict={
#     x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))




