import dwavebinarycsp as dbc;
import math;
from pymongo import MongoClient;
import numpy as np;
import pandas as pd;
from hybrid import State, States;
#from operators import Operator;


class QUnit(tuple):


	def __new__(self, phase, state):
		return tuple.__new__(self, tuple((phase, state)));


	def __init__(self, phase, state):
		if type(phase) == QUnit:
			self.phase = phase.phase;
			self.state = phase.state;
			self.config = phase.config;
		else:
			self.phase = phase;
			self.state = state;
			from qconfig import QConfig;
			self.config = QConfig();


	def set_config(self, config):
		self.config = config;


	def get_config(self):
		return self.config




	def split(self, amplitudes):
		split_index = int(len(self.state)/len(amplitudes));
		partition = sum(list(amplitudes));
		return (QUnit(amplitudes[i], self.state[i*split_index:(i+1)*split_index]) for i in range(len(ratio)));



	def __sub__(self, qb):
		return self.config.processor.__sub__(self, qb);


	def __add__(self, qb):
		return self.config.processor.__add__(self, qb);


	def __eq__(self, qb):
		return self.config.processor.__eq__(self, qb);


	def __mul__(self, a):
		return self.config.processor.__mul__(self, a);



	def __repr__(self):
		return str(self.phase)+"|"+str(self.state)+">";




	def bstate(self):
		return BState(self);



	def pstate(self):
		return PState(self);



	def gstate(self):
		return GState(self);



	def copy(self):
		return tuple(list(self).copy());


	def pspace(self):
		return PSpace(self);



	def hpspace(self):
		return HPSpace(self);



	def bspace(self):
		return BSpace(self);



	def hbspace(self):
		return HBSpace(self);



	def gspace(self):
		return GSpace(self);



	def hgspace(self):
		return HGSpace(self);



	def to_tuple(self):
		return tuple(self);



	def transpose(self):
		phase = complex(self.phase).conjugate();
		return QTUnit(phase, self.state);


	def t(self):
		return self.transpose();


	def to_bin(self):
		return "".join([bin(self.__getitem__(k))[2:] for k in range(len(self))]);


	def to_dna(self):
		dna=['A', 'G'];
		return "".join([dna[int(x)] for x in self.to_bin()]);




class QTUnit(QUnit):


	def __repr__(self):
		return "<"+str(self.state)+"|"+str(self.phase);



	def bstate(self):
		return "<"+self.to_bin()+"|";



	def pstate(self):
		return "<"+str(tuple(self))+"|";



	def transpose(self):
		phase = complex(self.phase).conjugate();
		return QUnit(phase, self.state);




class Space(QUnit):

	def __init__(self, qvalue):
		self.qvalue = qvalue




class State(QUnit):

	def __init__(self, qvalue):
		self.qvalue = qvalue




class PSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([self.qvalue.types[i](self.qvalue.values[i]) for i in range(len(self.qvalue.values))]).__repr__();





class HPSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([self.qvalue.types[i](self.qvalue.values[i]) for i  in range(2,len(self.qvalue.values)) ]).__repr__();





class BSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([str(math.ceil(math.log2(self.qvalue.processor.maxs[i]))-len(bin(self.qvalue.values[i])[2:]))+bin(self.qvalue.values[i])[2:] for i in range(len(self.qvalue.values))]).__repr__();




class HBSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([str(math.ceil(math.log2(self.qvalue.processor.maxs[i]))-len(bin(self.qvalue.values[i])[2:]))+bin(self.qvalue.values[i])[2:] for i in range(2, len(self.qvalue.values))]).__repr__();





class GSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([str(math.ceil(math.log2(self.qvalue.processor.maxs[i]))-len(bin(self.qvalue.values[i])[2:]))+bin(self.qvalue.values[i])[2:] for i in range(len(self.qvalue.values))]).__repr__();




class HGSpace(Space):

	def __repr__(self):
		qclass = type(self.qvalue)
		if  qclass == QUnit or qclass == QTUnit:
			return qclass([str(math.ceil(math.log2(self.qvalue.processor.maxs[i]))-len(bin(self.qvalue.values[i])[2:]))+bin(self.qvalue.values[i])[2:] for i in range(len(self.qvalue.values))]).__repr__();




class PState(State):


	def __repr__(self):
		pstate_value = str(tuple(self.qvalue))
		if type(self.qvalue) == QUnit:
			return "|"+pstate_value+">";
		if type(self.values) == QTUnit:
			return "<"+pstate_value+"|";




class BState(State):


	def __repr__(self):
		bstate_value = self.qvalue.to_bin()
		if type(self.qvalue) == QUnit:
			return "|"+bstate_value+">";
		if type(self.values) == QTUnit:
			return "<"+bstate_value+"|";




class GState(State):

	def __repr__(self):
		gstate_value = self.qvalue.to_dna()
		if type(self.qvalue) == QUnit:
			return "|"+gstate_value+">";
		if type(self.values) == QTUnit:
			return "<"+gstate_value+"|";





class QData(list):

	def __init__(self, states):
		if type(states) == tuple:
			states = list(states);
		if type(states) != list:
			states = [states];
		if type(states) == list:
			if len(states) > 0 and type(states[0]) == tuple:
				super(QData, self).__init__([QUnit(v[0], v[0:]) for v in states]);
			elif len(states) > 0 and type(states[0]) == QUnit:
				super(QData, self).__init__(states);
			self.states = states;


	def __getitem__(self, key):
		return super(QData, self).__getitem__(key);


	def __len__(self):
		return len(self.states);


	def __repr__(self):
		rep = ""
		for k in range(self.states.__len__()):
			if k != len(self.states)-1:
				rep = rep+str(self.states[k].phase)+"|"+str(self.states[k].state)+"> + \n";
			else:
				rep = rep+str(self.states[k].phase)+"|"+str(self.states[k].state)+">"
		return rep;


	def __mul__(self, a):
		return self.processor.__mul__(self, a);


	def __add__(self, a):
		return self.processor.__add__(self, a);



	def __sub__(self, a):
		return self.processor.__sub__(self, a);


	def __eq__(self, qb):
		return processor.__eq__(self, qb);


	def set_config(self, config):
		self.processor = config.processor;




	def pspace(self):
		qclass = type(self);
		return qclass([x.pspace() for x in self])




	def bspace(self):
		qclass = type(self);
		return qclass([x.bspace() for x in self])




	def gspace(self):
		qclass = type(self);
		return qclass([x.gspace() for x in self])




	def hpspace(self):
		qclass = type(self);
		return qclass([x.hbspace() for x in self])




	def hbspace(self):
		qclass = type(self);
		return qclass([x.hpspace() for x in self])




	def hgspace(self):
		qclass = type(self);
		return qclass([x.hgspace() for x in self])




	def pstate(self):
		qclass = type(self);
		return qclass([x.pstate() for x in self])




	def bstate(self):
		qclass = type(self);
		return qclass([x.bstate() for x in self])




	def gstate(self):
		qclass = type(self);
		temp = [x.gstate() for x in self];
		return qclass(temp)




	def transpose(self):
		return QTData([x.transpose() for x in self]);




	def t(self):
		return self.transpose();



	def condense(self):
		return self;


	def expand(self):
		return self;




class QTData(QData):


	def __getitem__(self, key):
		return self.states[key];


	def __repr__(self):
		rep = ""
		for k in range(self.states.__len__()):
			if k != len(self.states)-1:
				rep = rep+"<"+str(self.states[k].state)+str(self.states[k].phase)+"| + \n";
			else:
				rep = rep+"<"+str(self.states[k].state)+str(self.states[k].phase)+"|"
		return rep;


	def transpose(self):
		return QData([x.transpose() for x in self.states]);





class QSystem():



	def __init__(self, qT, H, q, config=None):
		self.qT=qT;
		self.H = H;
		self.q =q;
		from qconfig import QConfig;
		self.config = config if config != None else QConfig();



	def __repr__(self, a):
		"""
			< q | A | q > 

			< q | A | q > = expected value of A
			< q | I | q > = probability of state | q >

			processor: [Processor Representation]
			individual_processors:[ list of Processor Representation]

		"""
		return self.qT.__repr__()+self.H.__repr__()+self.q.__repr__()+"\n"+self.processor.__repr__();



	def __mul__(self, a):
		return self.config.processor.__mul__(self, a);



	def __add__(self, a):
		return self.config.processor.__add__(self, a);



	def __sub__(self, a):
		return self.config.processor.__sub__(self, a);



	def __div__(self, a):
		return self.config.rocessor.__div__(self, a);



	def __add__(self, a):
		return self.config.processor.__add__(self, a);



	def __mod__(self, a):
		return self.config.processor.__mod__(self, a);


	def __eq__(self, qb):
		return self.config.processor.__eq__(self, qb);



	def eval(self, sampler):
		return sampler.sample(bqm);



	def find_entanglements(self):
		pass



	def find_bindings(self):
		return self.find_entanglements();








class QEntangle(QData):


	def __init(self):
		pass
 
	def __init__(self, value):
		super(QEntangle, self).__init__();
		self.value = __check_value_is_valid__(value);



	def __repr__(self):
		"""
		['a=b'];
		['a=b']+['c=d']
		['a=b']*['c=d']
		['a=b']/['c=d']
		['a=b']//['c=d']
		['a=b']%['c=d']
		['a=b']%%['c=d']
		['a=b=c']
		['a=b=c']+[d=e]
		['a=b=c']*[d=e]
		['a=b=c']+[d=e]
		['a=b=c']/[d=e]
		['a=b=c']//[d=e]
		['a=b=c']%[d=e]
		['a=b=c']%%[d=e]
		"""
		return str([x for x in self.value]);


	def __check_value_is_valid__(self, value):
		try:
			return value;
		except Exception as e:
			raise e;




class QBind(QEntangle):
	"""docstring for QBind"""
	def __init__(self, arg):
		super(QBind, self).__init__()
		




class Quantumic(list, QSystem):
	"""
	QuantumIC is a list or sequence of Quantum Systems(QSystems) which some qubits are binded by quantum entanglement
	"""


	def __init__(self, bin_tuple_array=None, sample=None, state=None, value=[(0,)], n_qbits=(5,), index=[(0,0,0)], labels=({'a':2,'b':2,'c':3},)):
		"""
		bin_tuple_array: [(value in binary 0, concatenated binary indexes 0), (value in binary 1, concatenated binary indexes 1), ... ]
		"""
		self.labels = labels;
		self.sampler = sampler;
		self.value_indexes = list((tuple([value]+index)));
		if bin_tuple_array != None:
			self.from_bin_tuple_array(bin_tuple_array);
			super(Quantumic, self).__init__(bin_tuple_array);
		if sample != None:
			self.from_sample(sample);
		if state != None:
			self.from_state(state);
		else:
			self.state_str = self.value_indexes
			self.n_qbits = n_qbits;
			self.total_n_qbits = tuple([n_qbits[i]+sum([ math.log2(v) for k,v in labels[i].items()]) for i in range(len(n_qbits))])


	def __repr__(self):
		"""
		H | q1 >[ q1[a]=q1[b], q2[a]=q1[c] ]< q2 | G | q3 >

		< q0 | H [ q1[a]=q1[b], q2[a]=q1[c] ] G | q3 >

		< q0 | H | q1 >[ q1[a]=q1[b], q2[a]=q1[c] ]< q2 | G | q3 >

		< q0 | H | q1 >[ q1[a]=q1[b], q2[a]=q1[c] ]< q2 | G | q3 > = energy

		processor = [ Processor Representation]
		"""
		temp = ""
		for value in self.values:
			temp+=values.__repr__();
		return temp


	def __eq__(self, qb):
		return self.processor.__sub__(self, qb);


	def __sub__(self, qb):
		return self.processor.__sub__(self, qb);


	def __add__(self, qb):
		return self.processor.__add__(self, qb);



	def __mul__(self, a):
		return self.processor.__mul__(self, a);




	def __mul__(self, qb):
		product = Quantumic()
		if type(qb) == Quantumic:
			product.value_indexes = self.value_indexes+qb.value_indexes;
			product.state_str = product.value_indexes
			product.labels = self.labels+qb.labels;
			product.n_qbits = self.n_qbits+qb.n_qbits
			product.total_n_qbits = self.total_n_qbits + qb.total_n_qbits;
			return product
		elif type(qb) == Operator:
			return qb.leftDot(self);


	def __add__(self, qb):
		ADD=Operator().ADD;
		if type(qb) == Quantumic:
			addition_state = self*qb;
			return ADD*addition_state;




	def __sub__(self, qb):
		SUB=Operator().SUB;
		if type(qb) == Quantumic:
			addition_state = self*qb;
			return SUB*addition_state;

	

	def save(self, use_db=False):
		pass



	def dot(self, qb):
		#	Use Optimization Problem approach with DWave System.
		if type(qb) == Quantumic():
			def energy_function(qa, qb):
				pass;
			csp = dbc.Constraint(energy_function, self.labels(), dbc.BINARY, 'dot product');
			csp.add_values(self.to_dict());
			csp.add_values(qb.to_dict())
			bqm = dbc.stitch(csp);
			response = self.sampler.sample(bqm);
			response.energy();
		elif type(qb) == Operator():
			qb.leftDot(self);



	def add(self, qb):
		pass



	def fit(self, *args, **kwargs):
		pass



	def predict(self, *args, **kwargs):
		pass



	def evaluate(self, *args, **kwargs):
		pass



	def from_sample(self, sample):
		pass



	def from_state(self, state):
		pass



	def from_bin_tuple_array(self, bin_tuple_array):
		"""
		bin_tuple_array: [(value in binary 0, concatenated binary indexes 0), (value in binary 1, concatenated binary indexes 1), ... ]
		"""
		no_of_composites = len(bin_tuple_array);
		to_float = lambda v: v;
		to_int = lambda v: v;
		self.n_qbits = sum([len(bin_tuple_array[0][0]) for i in range(no_of_composites)]);
		self.value_indexes = list((to_int(bin_tuple_array[i][0]), to_int(bin_tuple_array[i][1])) for i in range(no_of_composites));
		self.total_n_qbits = tuple([len(bin_tuple_array[i][0]) + len(bin_tuple_array[i][1]) for i in range(no_of_composites)])




class Quantumics():

	def __init__(self, qOutputHibertspace, qOperator, qInputHilbertspace, config=None):
		if qInputClass == QSystem:
			self.system = qOutputClass;
		elif qInputClass == Quantumic:
			self.system = qOutputClass;
		elif qOutputClass == QData and qInputClass==QData:
			self.;
		elif qOutputClass == 
		from qconfig import QConfig;
		self.config = config if config != None else QConfig();



	def set_database(self, database):
		self.config.database = database if type(database) == q.QDatabase else None;




	def set_hilbertspace(self, hilbertspace):
		self.config.database = database if type(database) == q.QDatabase else None;



	def start(self):
		return self.config.server.start();



		








