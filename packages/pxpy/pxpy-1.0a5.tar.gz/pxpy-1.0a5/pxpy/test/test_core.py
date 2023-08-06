import ctypes
import sys
import time
import hashlib
import numpy as np
import pxpy as px
from pxpy import *
from tqdm import tqdm

lbar = None

def print_opt_state(state_p):
	state = state_p.contents
	global lbar
	if lbar is None:
		lbar = tqdm(total=state.max_iterations, mininterval=0.001, desc=px.Colors.TRAIN + 'TRAINING ' + px.Colors.ENDC)
	lbar.set_postfix_str(s=f"{state.obj:.4f}", refresh=True)
	lbar.update(1)
	if state.max_iterations == state.iteration:
		lbar = None

def print_progress_state(_cur,_tot,_nam):
	global lbar
	if lbar is None:
		lbar = tqdm(total=_tot, mininterval=0.001, desc=px.Colors.OTHER + _nam.decode('utf-8') + px.Colors.ENDC)
	lbar.update(1)
	if _cur == _tot:
		lbar.close()
		lbar = None

G = None

def squared_l2_regularization(state_p):
	global G
	state = state_p.contents

	# Graph access example
	# We cache the graph object in global var, because constructing the st_graph edgelist in every iteration will be slow
	if G is None:
		G = state.model.graph

	for i in range(state.dim):
		state.gradient[i] += 2.0 * 0.1 * state.weights[i]

def prox_l1(state_p):
	state = state_p.contents
	l = state.lam * state.stepsize
	for i in range(state.dim):
		x = state.weights_extrapolation[i] - state.stepsize * state.gradient[i]
		if x > l:
			state.weights[i] = x-l
		elif x < -l:
			state.weights[i] = x+l
		else:
			state.weights[i] = 0

#######################################################

def test_init():
	assert px.version() == 1

def test_recode():
	code = []
	ret = px.recode(code)
	assert ret == 0
	px.run()
	code = ['GPS \"THIS IS PX\";', 'NECHO GPS;', 'DEL GPS;']
	ret = px.recode(code)
	px.run()
	assert ret == 3

def test_register():
	px.write_register("LSN",4)
	assert px.read_register("LSN") == 4

def test_train_strf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	print(hashlib.sha1(D).hexdigest())

	model = px.train(data=D, iters=100, T=4, lam=0.33, graph=Graph.chain, mode=Mode.strf_rational, opt_proximal_hook=prox_l1, opt_regularization_hook=squared_l2_regularization)

	print(model.slice_edge(e=model.graph.edges-1,A=model.statistics))

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "305f3755d5e5e8926ed18f2727a2c97faec8d92d"
	assert abs(model.obj - 10.304831057652503) < 0.0001

	print(model.graph.nodes)

def test_train_mrf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	print(hashlib.sha1(D).hexdigest())

	model = px.train(data=D, iters=100, graph=Graph.auto_tree, mode=Mode.mrf)

	x = np.zeros(shape=(model.graph.nodes,))
	score = np.dot(model.weights, model.phi(x))

	print(model.slice_edge(e=model.graph.edges-1,A=model.statistics))
	#print(hashlib.sha1(model.slice_edge(e=model.graph.edges-1,A=model.statistics)).hexdigest())

	assert hashlib.sha1(model.slice_edge(e=model.graph.edges-1,A=model.statistics)).hexdigest() == "01d5b81d412908717198f197de24d3e1e39a800a"	
	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	assert abs(model.obj - 3.8664) < 0.0001
	assert abs(score - -41.3515) < 0.0001

def test_train_intmrf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, graph=Graph.auto_tree, k=6, mode=Mode.integer)

	probs, A = model.infer()

	#print("KL[empircal || estimate] = "+str(px.KL(model.statistics,probs)/model.graph.edges))

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	assert px.KL(model.statistics,probs)/model.graph.edges < 0.1
	assert model.obj == 9

def test_train_dbt():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, graph=Graph.auto, edge_fraction=0.1, mode=Mode.dbt)

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "d42c6bef1949377d6ca07c1528d8bd8e7f3a54e2"
	assert abs(model.obj - 4.8427) < 0.0001

def test_infer():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, inference=Inference.junction_tree, lam=0.1, graph=Graph.grid, mode=Mode.mrf, opt_proximal_hook=prox_l1)

	#print(np.linalg.norm(model.weights, ord=1))

	probs,  A_jt  = model.infer(inference=Inference.junction_tree)
	probs_jt = np.copy(probs)
	probs, A_lbp = model.infer(inference=Inference.belief_propagation)
	probs_lbp = np.copy(probs)
	probs, A_sqm = model.infer(inference=Inference.stochastic_quadrature, iterations=10000)
	probs_sqm = np.copy(probs)

	assert px.KL(probs_jt,probs_lbp)/model.graph.edges < 0.1
	assert px.KL(probs_jt,probs_sqm)/model.graph.edges < 0.1

	#print("Average KL of estimated edge marginals:")
	#print("KL[jt || lbp] = "+str(px.KL(probs_jt,probs_lbp)/model.graph.edges))
	#print("KL[jt || sqm] = "+str(px.KL(probs_jt,probs_sqm)/model.graph.edges))
	#print("Log-partition function values:")
	#print("A_jt="+str(A_jt) + ", A_lbp=" + str(A_lbp) + ", A_sqm=" + str(A_sqm))

def test_load_model():
	model = px.load_model(px.example_model_filename)

	assert model.graph.nodes == 784
	assert model.graph.edges == 783
	assert model.dim == 3132

def test_optimization_hooks():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, graph=Graph.chain, mode=Mode.mrf, opt_progress_hook=print_opt_state)
	l1_ml = np.linalg.norm(model.weights, ord=1)
	l2_ml = np.linalg.norm(model.weights, ord=2)

	model = px.train(data=D, iters=100, graph=Graph.chain, mode=Mode.mrf, opt_progress_hook=print_opt_state, opt_regularization_hook=squared_l2_regularization)
	l1_sl2reg = np.linalg.norm(model.weights, ord=1)
	l2_sl2reg = np.linalg.norm(model.weights, ord=2)

	model = px.train(data=D, iters=100, graph=Graph.chain, mode=Mode.mrf, opt_progress_hook=print_opt_state, opt_proximal_hook=prox_l1, lam=0.1)
	l1_l1reg = np.linalg.norm(model.weights, ord=1)
	l2_l1reg = np.linalg.norm(model.weights, ord=2)

	#print("L1: " + str(l1_ml) + " " + str(l1_sl2reg) + " " + str(l1_l1reg))
	#print("L2: " + str(l2_ml) + " " + str(l2_sl2reg) + " " + str(l2_l1reg))

	assert l1_ml > l1_sl2reg and l1_sl2reg > l1_l1reg
	assert l2_ml > l2_sl2reg and l2_sl2reg > l2_l1reg

def test_predict():
	model = px.load_model(px.example_model_filename)
	x = -np.ones(shape=(1,model.graph.nodes), dtype=np.uint16)
	model.predict(x)
	assert hashlib.sha1(x).hexdigest() == "73b34c93f9294d1b8dcbe1f75ecd3a2fcc3d004c"

def test_sampler():
	model = px.load_model(px.example_model_filename)

	np.set_printoptions(threshold=sys.maxsize)

	px.set_seed(1337)

	A = model.sample(sampler=Sampler.apx_perturb_and_map, num_samples=2)
	B = model.sample(sampler=Sampler.gibbs, num_samples=2)

	#print("PAM")
	#print(A.reshape(2,28,28).astype(np.uint16))
	#print("GIBBS")
	#print(B.reshape(2,28,28).astype(np.uint16))

	assert hashlib.sha1(A).hexdigest() == "42065cd73a460cb30eed3b8f597f933610086772"
	assert hashlib.sha1(B).hexdigest() == "51bfa48f594e70e16a1a37e4c8f422103357bb3e"

def test_custom_graph():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	E = np.array([0,1,0,2,0,3,0,4,0,5,0,6,0,7,0,8,0,9,0,10,0,11,0,12,0,13,0,14,0,15]).reshape(15,2)
	model = px.train(data=D, iters=100, graph=E, mode=Mode.mrf, opt_progress_hook=print_opt_state)
	assert hashlib.sha1(model.graph.edgelist).hexdigest() == hashlib.sha1(E).hexdigest()
