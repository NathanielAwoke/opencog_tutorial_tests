
import unittest
from opencog.atomspace import AtomSpace, types,TruthValue,Atom
from opencog.atomspace import types
from opencog.scheme_wrapper import scheme_eval, scheme_eval_h
from opencog.utilities import initialize_opencog
from opencog.type_constructors import *
from opencog.bindlink import satisfying_set


'''
Unit test for the tutorial Manipulating Atoms in Python 
http://wiki.opencog.org/w/Manipulating_Atoms_in_Python

'''




class Manipulating_atoms_in_python(unittest.TestCase):



    def setUp(self):
        self.atsp = AtomSpace()
        self.TV = TruthValue() 
        

    def test_making_atoms_cPlusPlus_syntax(self):
      cat = self.atsp.add_node(types.ConceptNode, "Cat")
      man = self.atsp.add_node(types.ConceptNode, "Man")
      animal = self.atsp.add_node(types.ConceptNode, "Animal")

      self.assertIsInstance(cat,Atom,"Not able to create node") # checks if the above created nodes are instances of Atom class

      print "Printing individual atoms in the atomspace"
      for atom in self.atsp:
        print atom




    def test_add_links_into_atomspace(self):
      man = self.atsp.add_node(types.ConceptNode, "Man")
      animal = self.atsp.add_node(types.ConceptNode, "Animal") 
      inheritance_link = self.atsp.add_link(types.InheritanceLink, [man,animal]) 
      self.assertIsInstance(inheritance_link,Atom,"Link not added to atomspace")


    def test_pattern_matching(self):

      #test pattern maching between difetent types of nodes
        initialize_opencog(self.atsp)
        self.scheme_animals = \
        '''
        (InheritanceLink (ConceptNode "Red") (ConceptNode "color"))
        (InheritanceLink (ConceptNode "Green") (ConceptNode "color"))
        (InheritanceLink (ConceptNode "Blue") (ConceptNode "color"))
        (InheritanceLink (ConceptNode "Spaceship") (ConceptNode "machine"))
        '''
        # create amodule or function in scheme 
        self.scheme_query = \
        '''
        (define find-colors
        (BindLink
            ;; The variable to be bound
            (VariableNode "$xcol")

            ;; The pattern to be searched for
            (InheritanceLink
            (VariableNode "$xcol")
            (ConceptNode "color")
            )
            ;; The value to be returned.
            (VariableNode "$xcol")
        )
        )
        '''
        #use scheme module
        scheme_eval(self.atsp, "(use-modules (opencog))") 
        scheme_eval(self.atsp, "(use-modules (opencog query))")
        scheme_eval_h(self.atsp, self.scheme_animals)
        scheme_eval_h(self.atsp, self.scheme_query)
        self.result = scheme_eval_h(self.atsp, '(cog-bind find-colors)')   
        self.varlink = TypedVariableLink(VariableNode("$xcol"), TypeNode("ConceptNode"))
        self.pattern = InheritanceLink(VariableNode("$xcol"), self.test_color)
        self.colornodes = SatisfactionLink(self.varlink, self.pattern)
        self.assertEqual(self.result,satisfying_set(self.atsp, self.colornodes))
      
	

    def test_making_atoms_scheme_syntax(self):

      pass

    



   
if __name__ == '__main__':
    unittest.main()




