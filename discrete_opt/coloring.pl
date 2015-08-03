:- module(coloring).
:- export colour/2, main/2.

:- lib(regex). % needed for split
:- lib(ic). % for integer constraints

%% read in a list of edges; index-0
rows_read(Res, Num_nodes, Num_edges, Filename) :-
    open(Filename, read, Stream),
    read_string(Stream, end_of_line, _, Header), % header
    %% split Header on ' ' with [] options into Parts, which includes ' ' but is to be ignored
    split(' ', Header, [], [Tmp_Num_nodes, _, Tmp_Num_edges]),
    number_string(Num_nodes, Tmp_Num_nodes), % convert from str to num
    number_string(Num_edges, Tmp_Num_edges),
    rows_read_inner(0, Num_edges, Stream, [], ResRev),
    reverse(Res, ResRev),
    close(Stream).


rows_read_inner(N, N, Stream, Acc, Acc). % terminal condition
rows_read_inner(I, Num_edges, Stream, Acc, Res) :-
    read_string(Stream, end_of_line, _, Row),
    split(' ', Row, [], [Tmp_U0, _, Tmp_U1]),
    number_string(U0, Tmp_U0),
    number_string(U1, Tmp_U1),
    I_new is I +1,
    rows_read_inner(I_new, Num_edges, Stream, [(U0, U1)|Acc], Res).


%% add in all edge constraints
pairwise_diff([(L,R)|T], Variables) :-
    % edges are index-0, but variables' range start at 1.
    L_tmp is L +1, R_tmp is R +1,
    Variables[L_tmp] #\= Variables[R_tmp], % Variable[L_tmp] cannot unify with Variable[R_tmp]
    pairwise_diff(T, Variables).
pairwise_diff([], Variables).


colour(Colours, Filename) :-
    %% read in data
    rows_read(Res, Num_nodes, Num_edges, Filename),
%    length(Variables, Num_nodes), % does not allow subscript, ie. Variable[2] #= 2 would give an instantiation fault
    %% setup constraints
    dim(Colours, [Num_nodes]),
    Colours #:: 1..Num_nodes, % all Colours take integer values between 1 and Num_nodes
    pairwise_diff(Res, Colours),
    %% search
    search(
        % src: http://eclipseclp.org/docs/current/bips/lib/ic/search-6.html
        Colours, % list of domain variables (when Arg = 0)
        0, % Arg
        first_fail, % "the entry with the smallest domain size is selected"
        indomain_min, % "Values are tried in increasing order. On failure, the previously tested value is removed. The values are tested in the same order as for indomain, but backtracking may occur earlier."
        complete, % "a complete search routine which explores all alternative choices"
        [] % none
    ).


main(InputFilename, OutputFilename) :-
    colour(Colours, InputFilename),
    open(OutputFilename, write, Stream),
    dim(Colours, [DimColours]),
    ic:max(Colours, NumColours), % assumes labels start at 1 % TODO: check, or properly count the number of distinct elements
    write(Stream, NumColours), write(Stream, ' 0\n'),
    (
        for(R,1,DimColours),
        param(Colours, Stream)
    do
        Val is Colours[R] -1, % so to take the value out of the array % index-0
        write(Stream, Val),
        write(Stream, ' ')
    ),
    close(Stream),
    !. % no backtracking after this, otherwise it will search for more answers