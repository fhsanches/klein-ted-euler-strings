# klein-ted-euler-strings
An implementation of Klein's algorithm for the Tree Edit Distance (TED) problem using Euler Strings, as described in his original work (Klein, 1998).

Notice: This implementation is provided for study and research purposes. If you require an efficient solution for the TED problem, I'd suggest checking Pawlik&Augsten APTED.

Other implementations of Klein's algorithm usually are an modified version of Zhang-Shasha using a specific Strategy. This implementation, however, converts the trees into Euler Strings and computes a restricted version of the Levenshtein Distance (Levenshtein, 1965).

Details of implementation can be found in my Master's thesis (Sanches, Fernando H. Analise de Algoritmos para o Problema de Distância de Edição de Árvores. The text was written in English.) - feel free to ask me for a digital copy.

Usage: 
Input trees must be given as a dictionary representing adjacency lists. For each pair (key, values) in the dict, key is the label of a node in the tree, and value is a list containing the labels of its children. See example.py for usage.

If you want to customize the cost functions, you may extend the "Cost" class with the "cdel" and "cmatch" methods, as shown in the example.

*Files description:*
- klein.py: the algorithm itself, and related data structures;
- klein_test.py: unit tests.

*Known bugs:*
- More comprehensive test sets should be implemented;
- The recursion reaches the stack depth faster than it should (can be mitigated with a sys.setrecursionlimit(100000)
at the beginning of the program).
- Inputting nodes and labels should be done sepparately (to allow repeat labels);
- Documentation is still a WIP.

Warning: The performance for this algorithm grows quickly, specially in space.
