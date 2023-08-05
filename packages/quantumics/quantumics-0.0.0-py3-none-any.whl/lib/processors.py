import dwavebinarycsp as dbc;
from qiskit import ClassicalRegister as CR, QuantumRegister as QR, QuantumCircuit as QC
import math;
from dwave.system.samplers import DWaveSampler;
from qiskit import IBMQ, backends;
from hybrid import State, States;
from pymongo import MongoClient;
import numpy as np;
import sklearn as skl;
import qsharp
from qoperators import QOperator;
from quantumics import QUnit, QTUnit, QData, QTData;
#import Microsoft.Samples as ms




class QDatabase():

	def __init__(self, url):
		self.url = url;






class Processor():

	def __init__(self, mins=[0,0,0,0], database=QDatabase('mongodb://localhost:7000'), 
		maxs=[16, 16, 16, 16], delayed=False):
		self.delayed = delayed
		self.maxs = maxs;
		self.mins = mins;
		self.database = database;




	def __mul__(self, a, b):
		return self.dot(a, b);



	def __add__(self, a, b):
		return self.add(a, b);



	def __sub__(self, a, b):
		return self.sub(a, b);



	def __eq__(self, a, b):
		if type(a) != QUnit and type(b)==QUnit:
			return QEntangle(a, qb);



	def dot(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if (type(qa)== QUnit or type(qa) == QTUnit) and (type(qb)== QUnit or type(qb) == QTUnit):
			return self.unit_mul(qa, qb);
		elif (type(qa)== QData or type(qa) == QTData) and (type(qb)== QData or type(qb) == QTData):
			return self.data_mul(qa, qb);
		elif type(qa)== QOperator and type(qb)==QUnit:
			return self.operator_qunit(qa, qb);
		elif type(qa)== QOperator and type(qb)==QOperator:
			return self.operator_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QOperator:
			return self.qtunit_operator(qa, qb);
		elif type(qa)== QOperator and type(qb)==QData:
			return self.operator_qdata(qa, qb);
		elif type(qa)== QTData and type(qb)==QOperator:
			return self.qtdata_operator(qa, qb);




	def div(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa)== QUnit and type(qb)==QUnit:
			return self.qunit_mul(qa, qb);
		elif type(qa)== Operator and type(qb)==QUnit:
			return self.operator_qunit(qa, qb);
		elif type(qa)== Operator and type(qb)==Operator:
			return self.operator_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==Operator:
			return self.qtunit_operator(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QTUnit:
			return self.qtunit_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QUnit:
			return self.qtunit_qunit(qa, qb);
		elif type(qa)== QUnit and type(qb)==QTUnit:
			return self.qunit_qtunit(qa, qb);
		elif type(qa)== QData and type(qb)==QData:
			return self.qdata_mul(qa, qb);
		elif type(qa)== Operator and type(qb)==QData:
			return self.operator_qdata(qa, qb);
		elif type(qa)== QTData and type(qb)==Operator:
			return self.qtdata_operator(qa, qb);
		elif type(qa)== QTData and type(qb)==QTData:
			return self.qtdata_mul(qa, qb);
		elif type(qa)== QTData and type(qb)==QData:
			return self.qtdata_qdata(qa, qb);
		elif type(qa)== QData and type(qb)==QTData:
			return self.qdata_qtdata(qa, qb);



	def add(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa) != type(qb):
			raise Exception();
		elif type(qa) == type(qb):
			if type(qa) == QOperator:
				return self.operator_add(qa, qb);
			elif type(qa) == QUnit or type(qa) == QTUnit:
				return self.unit_add(qa, qb);
			elif type(qa) == QData(qa, qb) or type(qa) == QTData:
				return self.data_add(qa, qb);
			elif type(qa) == Quantumic(qa, qb):
				return self.quantumic_add(qa, qb);
			elif type(qa) == QEntangle or type(qa) == QBind:
				return self.qentangle_add(qa, qb);
			elif type(qa) == QSystem(qa, qb):
				return self.qsystem_add(qa, qb);
			elif type(qa) == Quantumics(qa, qb):
				return self.quantumics_add(qa, qb);



	def sub(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa) != type(qb):
			raise Exception();
		elif type(qa) == type(qb):
			if type(qa) == QOperator:
				return self.operator_sub(qa, qb);
			elif type(qa) == QUnit or type(qa) == QTUnit:
				return self.unit_sub(qa, qb);
			elif type(qa) == QData(qa, qb) or type(qa) == QTData:
				return self.data_sub(qa, qb);
			elif type(qa) == Quantumic(qa, qb):
				return self.quantumic_sub(qa, qb);
			elif type(qa) == QEntangle or type(qa) == QBind:
				return self.qentangle_sub(qa, qb);
			elif type(qa) == QSystem(qa, qb):
				return self.qsystem_sub(qa, qb);
			elif type(qa) == Quantumics(qa, qb):
				return self.quantumics_sub(qa, qb);


	def train(self, *args, **kwargs):
		return self.hamiltonian(*args, **kwargs)



	def fit(self, *args, **kwargs):
		return self.hamiltonian(*args, **kwargs);




	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		"""
		"""
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class DNAProcessor(Processor):


	def __init__(self, *args, **kwargs):
		super(DNAProcessor, self).__init__();
		for k in kwargs:
			self[k] = kwargs[k];



	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		"""
		"""
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass







class CPUProcessor(DNAProcessor):


	def train(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);



	def fit(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);


	def __repr__(self):
		pass


	def eval(self, a):
		pass



	def hamiltonian(self, operator=None, model=None, eigenmatrix=None, metric_basis=None, dataset=None, eingenfunction=None, file=None):
		if operator != None:
			return operator;
		if model == None:
			pass
		else:
			return QOperator(model, metric_basis=metric_basis);



	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		"""
		"""
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass



	def unit_add(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				return typer(qa.phase + qb.phase, qb.state);
			else:
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);


	def operator_add(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.phases + qb.phases, qb.states);



	def unit_sub(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				return typer(qa.phase - qb.phase, qb.state);
			else:
				qb.phase = - qb.phase;
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);



	def operator_sub(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.phases - qb.phases, qb.states);



	def unit_mul(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if type(qa) == type(qb): 
				return typer(qa.phase*qb.phase, (qa.state, qb.state))
			elif type(qa) == QUnit and type(qb) == QTUnit:
				a = QUnit(1, qa.state); b = QUnit(1, qb.state);
				return QOperator([[qa.phase*qb.phase]], metrics=QOperatorMetrics([[(a,b)]]))
			elif type(qa) == QTUnit and type(qb) == QUnit:
				return qa.phase*qb.phase*qa.config.get_metric(qa.state, qb.state);
			elif (type(qa) != QTUnit and type(qa)) != QUnit and (type(qb) == QTUnit or type(qb) == QUnit):
				return type(qb)(qa*qb.phase, qb.state);
			elif (type(qb) != QTUnit and type(qb)) != QUnit and (type(qa) == QTUnit or type(qa) == QUnit):
				return type(qa)(qb*qa.phase, qa.state);



	def operator_mul(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.phases * qb.phases, qb.states);





	def data_add(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == typer(qb):
				sub_typer = type(qa[0]);
				states = list(set(qa.states.concat(qb.states)));
				return typer([sub_typer(qa.phases[qa.index(k)] + qa.phases[qa.index(k)]) for k in states ]);
			else:
				raise Exception();



	def data_sub(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == typer(qb):
				sub_typer = type(qa[0]);
				states = list(set(qa.states.concat(qb.states)));
				return typer([sub_typer(qa.phases[qa.index(k)] - qa.phases[qa.index(k)]) for k in states ]);
			else:
				raise Exception();


	def data_mul(self, qa, qb):
		if type(qa) == QData and type(qb) ==QTData:
			return self.data_outer_product(qa, qb);
		elif type(qa) == QTData and type(qb) ==QData:
			return self.data_inner_product(qa, qb);
		elif (type(qa) == QData and type(qb) ==QData) or (type(qa) == QTData and type(qb) == QTData) :
			return self.data_outer_product(qa, qb);
			


	def data_outer_product(self, qa, qb):
		return QOperator([[],[]],[[],[]])



	def data_inner_product(self, qa, qb):
		pass


	def data_tesnsor_product(self, qa, qb):
		pass


"""


class GPUProcessor(DNAProcessor):

	def __init__(self, a):
		pass

	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class IBMQProcessor(DNAProcessor):

	def __init__():
		pass

	def __mul__(self, a, b):
		pass


	def test(self):
		return ms.HelloQ.simulate();


	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class MsQProcessor(DNAProcessor):

	def __init__(self):
		super(MsQProcessor, self).__init__();


	def __mul__(self, a, b):
		return self.ms.MUL.simulate(stateA=a, stateB=b)


	def __add__(self, a, b):
		return self.ms.ADD.simulate(stateA=a, stateB=b)


	def __sub__(self, a, b):
		return self.ms.SUB.simulate(stateA=a, stateB=b)


	def __div__(self, a, b):
		return self.ms.DIV.simulate(stateA=a, stateB=b)


	def exp(self, a, b):
		return self.ms.EXP.simulate(stateA=a, stateB=b)



	def pow(self, a, b):
		return self.ms.POW.simulate(stateA=a, stateB=b);


	def train(self, a, b):
		return self.ms.TRAIN.simulate(stateA=a, stateB=b);



	def hamiltonian(self, a, b):
		return self.ms.HAMILTONIAN.simulate(stateA=a, stateB=b);



	def fft(self, a):
		return self.ms.FFT.simulate(stateA=a);


	def pca(self, a):
		return self.ms.PCA.simulate(stateA=a);


	def svd(self, a):
		return self.ms.SVD.simulate(stateA=a);



	def eval(self, a):
		return self.ms.FFT.simulate(stateA=a);



	def identity(self, a):
		return self.ms.IDENTITY.simulate(state=a);



	def hammard(self, a):
		return self.ms.HAMMARD.simulate(state=a);



	def cnot(self, a, b):
		return self.ms.CNOT.simulate(stateA=a, stateB=b);



	def qand(self, a, b):
		return self.ms.AND.simulate(stateA=a, stateB=b);



	def qor(self, a, b):
		return self.ms.OR.simulate(stateA=a, stateB=b);





class DWaveQProcessor(DNAProcessor):


	def __mul__(self, a, b):
		return self.rightDot(a, b);



	def __add__(self, a, b):
		return self.rightAdd(a, b);




	def __sub__(self, a, b):
		return self.rightSub(a, b);

 



	def qunit_mul(self, qa, qb):
		product = Quantumic()
		product.value_indexes = self.value_indexes+qb.value_indexes;
		product.state_str = product.value_indexes
		product.labels = self.labels+qb.labels;
		product.n_qbits = self.n_qbits+qb.n_qbits
		product.total_n_qbits = self.total_n_qbits + qb.total_n_qbits;
		pass


	

	def quint_add(self, qa, qb):
		pass



	
	def quint_sub(self, qa, qb):
		pass



	def qtunit_mul(self, qa, qb):
		pass


	

	def qtuint_add(self, qa, qb):
		pass



	
	def qtuint_sub(self, qa, qb):
		pass



	def qtunit_qunit(self, qa, qb):
		pass



	def qunit_qtunit(self, qa, qb):
		pass



	def qdata_mul(self, qa, qb):
		pass


	

	def qdata_add(self, qa, qb):
		pass



	
	def qdata_sub(self, qa, qb):
		pass



	def qtdata_qdata(self, qa, qb):
		pass



	def qdata_qtdata(self, qa, qb):
		pass


	
	def operator_mul(self, qa, qb):
		pass


	
	def operator_add(self, qa, qb):
		pass



	def operator_sub(self, qa, qb):
		pass



	def operator_qunit(self, o, qa):
		pass




	def qtunit_operator(self, qa, o):
		pass



	def train():
		pass;



	def evaluate(self):
		pass

		


	def leftDot(self, qa, qb):
		if type(qa) == QUnit:
			self.bqm.add_variables(quantumic.to_dict());
			quantumic = Quantumic(sampler.samples(self.bqm));
			return quantumic
		elif type(quantumic) == Operator:
			pass



	def rightDot(self, qa, qb):
		if type(qa) == QUnit:
			self.bqm.add_variables(qa.to_dict());
			self.bqm.add_variables(q)
			quantumic = Quantumic(sampler.samples(self.bqm));
			return quantumic
		elif type(qa) == Operator:
			pass
		


	def rightAdd(self, qa, qb):
		ADD=Operator().ADD;
		if type(a) == QUnit:
			addition_state = a*b;
			return ADD*addition_state;




	def rightAdd(self, qa, qb):
		if type(quantumic) == Quantumic:
			self.bqm.add_variables(quantumic.to_dict());
			quantumic = Quantumic(sampler.samples(self.bqm));
			return quantumic
		elif type(quantumic) == Operator:
			pass



	def leftAdd(self, qa, qb):
		if type(quantumic) == Quantumic:
			self.bqm.add_variables(quantumic.to_dict());
			quantumic = Quantumic(sampler.samples(self.bqm));
			return quantumic
		elif type(quantumic) == Operator:
			pass



	def rightSub(self, qa, qb):
		SUB=Operator().SUB;
		if type(a) == QUnit:
			addition_state = a*b;
			return SUB*addition_state;





class IDQProcessor(DWaveQProcessor, IBMQProcessor):

	def __init__():
		pass

	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class MDQProcessor(DWaveQProcessor, MsQProcessor):

	def __init__():
		pass


	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class IMQProcessor(IBMProcessor, MsQProcessor):

	def __init__():
		pass


	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class IMDQProcessor(MsProcessor, DWaveProcessor, IBMProcessor):

	def __init__():
		pass


	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):

		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass





class Map():

	def __init__():
		pass





class DNABinMap(Map):


	def __init__(self, dna, bin):
		pas

"""

