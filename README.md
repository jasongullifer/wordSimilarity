Compute Word Similarity
Jason Gullifer (jason.gullifer@gmail.com) - 2009

Levenshtein Distance algorithm taken from
http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distancePython

This program computes two word similarity measures: 1) a
modified version of the Van Orden orthographic similarity measure
(Van Orden, 1987) for a pairs of words, and 2) a normalized
Levenshtein Distance measure (Schepens, Dijkstra, & Grootjen, 2011).

Van Orden, G. C. (1987). A ROWS is a ROSE: Spelling, sound, and
reading. Memory & Cognition, 15(3), 181-198. 

Schepens, J., Dijkstra, T., & Grootjen, F. (2011). Distributions of
cognates in Europe as based on Levenshtein distance. Bilingualism:
Language and Cognition, 15(01),
157-166. doi:10.1017/S1366728910000623

Usage: python wordSimilarity.py

input.csv should be a comma separated file with two columns. Each
row should contain your target word and the word it should be
compared with. No column names should be included. The result will
be an output file called output_wordSim.csv that contains each word
pair, its normalized Levenshtein Distance, and its orthographic
similarity.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.



