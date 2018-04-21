
trait_length = 20
sets_desired = 80

trait_sets = []
targets = []
sequences = [] #should be 2D list with all sequences


"""
Should load all DNA sequences into 'sequences' as numbers.
    _ = 0    
    A = 1
    T = 2
    C = 3
    G = 4
"""
def load_data_into_sequences():
    """
    Will read from fasta file and fill sequences
    """
    


"""
Each list inside trait_sets will include a set of bases,
vertically extracted sequences.

Example:    If we have these sequences:

            AATC
            TATG
            ATAC
            TTTG

            the first trait set will be [1, 2, 1] with a
            target of 2 (see load_data_into_sequences for
            letter to number mapping)
"""
def load_sequences_into_traits():
    #assuming all sequences have equal size
    seq_length = len(sequences[0])

    for i in range(seq_length):
        for j in range(sets_desired):
            trait_set = []
            for k in range(trait_length):

                base = sequences[j+k][i]
                trait = 0

                if base == 'a':
                    trait = 1
                elif base == 't':
                    trait = 2
                elif base == 'c':
                    trait = 3
                elif base == 'g':
                    trait = 4

                trait_set.append(trait)

            trait_sets.append(trait_set)
            targets.append(sequences[j + trait_length][i])
            
def main():
    """
    Code goes here
    """
main()