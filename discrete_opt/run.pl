:- use_module(coloring).

%% cannot call functions in coloring.pl because eclipse-clp gives the error
%% "(68) calling an undefined procedure\n When called from Prolog.",
%% that is, a module and script cannot be mixed.