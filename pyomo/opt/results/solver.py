#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

__all__ = ['SolverInformation', 'SolverStatus', 'TerminationCondition']

from pyutilib.enum import Enum
from pyomo.opt.results.container import MapContainer, ScalarType


#
# A coarse summary of how the solver terminated.
#
SolverStatus = Enum(
    'ok',                   # Normal termination
    'warning',              # Termination with unusual condition
    'error',                # Terminated internally with error
    'aborted',              # Terminated due to external conditions
                            #   (e.g. interrupts)
    'unknown'               # An unitialized value
    )

#
# A description of how the solver terminated
#
TerminationCondition = Enum(
    # UNKNOWN
    'unknown',                 # An unitialized value
    # OK
    'maxTimeLimit',            # Exceeded maximum time limited allowed by user
                               #    but having return a feasible solution
    'maxIterations',           # Exceeded maximum number of iterations allowed
                               #    by user (e.g., simplex iterations)
    'minFunctionValue',        # Found solution smaller than specified function
                               #    value
    'minStepLength',           # Step length is smaller than specified limit
    'globallyOptimal',         # Found a globally optimal solution
    'locallyOptimal',          # Found a locally optimal solution
    'feasible',                # Found a solution that is feasible
    'optimal',                 # Found an optimal solution
    'maxEvaluations',          # Exceeded maximum number of problem evaluations
                               #    (e.g., branch and bound nodes)
    'other',                   # Other, uncategorized normal termination
    # WARNING
    'unbounded',               # Demonstrated that problem is unbounded
    'infeasible',              # Demonstrated that the problem is infeasible
    'infeasibleOrUnbounded',   # Problem is either infeasible or unbounded
    'invalidProblem',          # The problem setup or characteristics are not
                               #    valid for the solver
    'intermediateNonInteger',  # A non-integer solution has been returned
    'noSolution',              # No feasible solution found but infeasibility
                               #    not proven
    # ERROR
    'solverFailure',           # Solver failed to terminate correctly
    'internalSolverError',     # Internal solver error
    'error',                   # Other errors
    # ABORTED
    'userInterrupt',           # Interrupt signal generated by user
    'resourceInterrupt',       # Interrupt signal in resources used by
                               #    optimizer
    'licensingProblems'        # Problem accessing solver license
    )


class BranchAndBoundStats(MapContainer):

    def __init__(self):
        MapContainer.__init__(self)
        self.declare('number of bounded subproblems')
        self.declare('number of created subproblems')


class BlackBoxStats(MapContainer):

    def __init__(self):
        MapContainer.__init__(self)
        self.declare('number of function evaluations')
        self.declare('number of gradient evaluations')
        self.declare('number of iterations')


class SolverStatistics(MapContainer):

    def __init__(self):
        MapContainer.__init__(self)
        self.declare("branch_and_bound", value=BranchAndBoundStats(),
                     active=False)
        self.declare("black_box", value=BlackBoxStats(), active=False)


class SolverInformation(MapContainer):

    def __init__(self):
        MapContainer.__init__(self)
        self.declare('name')
        self.declare('status', value=SolverStatus.ok)
        # Semantics: the integer return code from the shell in which the solver
        # is launched.
        self.declare('return_code')
        self.declare('message')
        self.declare('user_time', type=ScalarType.time)
        self.declare('deterministic_time', type=ScalarType.float)
        self.declare('system_time', type=ScalarType.time)
        self.declare('wallclock_time', type=ScalarType.time)
        # Semantics: The specific condition that caused the solver to
        # terminate.
        self.declare('termination_condition',
                     value=TerminationCondition.unknown)
        # Semantics: A string printed by the solver that summarizes the
        # termination status.
        self.declare('termination_message')
        self.declare('statistics', value=SolverStatistics(), active=False)
        self.declare('warm_start_objective_value', type=ScalarType.float)
        # Semantics: The total time spent processing the root node.
        self.declare('root_node_processing_time', type=ScalarType.time)
        # Semantics: The total time spent processing the MIP search tree.
        self.declare('tree_processing_time', type=ScalarType.time)
        # Semantics: The total time spent processing the MIP search tree.
        self.declare('n_solutions_found', type=ScalarType.int)
