from .gtftools import GtfFeature
from .gfftools import GffFeature


def gtf_to_generic_feature(gtf_feature):
    """
    Covert GtfFeature (namedtuple) to GenericFeature

    Args:
        gtf_feature: GtfFeature object
    """
    f = gtf_feature

    attr_list = []
    for a in f.attribute.split(';'):
        key = a.split(' "')[0]
        val = a[len(key)+2:-1]
        attr_list.append((key, val))

    return GenericFeature(
        seqname=f.seqname,
        type_=f.feature,
        start=f.start,
        end=f.end,
        strand=f.strand,
        attributes=attr_list,
        frame=f.frame + 1
    )


def gff_to_generic_feature(gff_feature):
    """
    Covert GffFeature (namedtuple) to GenericFeature

    Args:
        gff_feature: GffFeature object
    """
    f = gff_feature
    items = [item for item in f.attributes.split(';') if item]

    attr_list = []
    for item in items:
        key, val = item.split('=')
        attr_list.append((key, val))

    return GenericFeature(
        seqname=f.seqid,
        type_=f.type,
        start=f.start,
        end=f.end,
        strand=f.strand,
        attributes=attr_list,
        frame=1 if f.phase == '.' else f.phase + 1
    )


def generic_to_gtf_feature(generic_feature):
    """
    Covert GenericFeature to GtfFeature (namedtuple)

    Args:
        generic_feature: GenericFeature object
    """
    f = generic_feature

    # Pack attributes into a single line of str
    attr_str = ''
    for key, val in f.attributes:
        if type(val) is int or type(val) is float:
            attr_str += f"{key} {val};"
        else:  # type(val) is str -> Add quote ""
            val = val.replace(';', '<semicolon>')  # semicolon is not allowed in the GTF attribute field
            attr_str += f"{key} \"{val}\";"

    return GtfFeature(
        seqname=f.seqname,
        source='.',
        feature=f.type,
        start=f.start,
        end=f.end,
        score='.',
        strand=f.strand,
        frame=f.frame - 1,  # GTF frame is 0, 1, 2
        attribute=attr_str[:-1]  # Remove trailing ';'
    )


def generic_to_gff_feature(generic_feature):
    """
    Covert GenericFeature to GffFeature (namedtuple)

    Args:
        generic_feature: GenericFeature object
    """
    f = generic_feature

    # Pack attributes into a single line of str
    attr_str = ''
    for key, val in f.attributes:
        # Escape characters not allowed
        val = val.replace(';', '%3B').replace('=', '%3D')
        attr_str += f"{key}={val};"

    return GffFeature(
        seqid=f.seqname,
        source='.',
        type=f.type,
        start=f.start,
        end=f.end,
        score='.',
        strand=f.strand,
        phase=f.frame - 1,  # GFF frame is 0, 1, 2
        attributes=attr_str[:-1]  # Remove trailing ';'
    )


class GenericFeature:
    """
    Data class designed to store features from Genbank and GTF files.

    Instance attributes:
        seqname: str
            The unique name of chromosome, genome or contig to which this feature belongs

        type: str
            The type of the feature, e.g. 'CDS', 'tRNA', 'misc_feature'

        start: int
            1-based inclusive

        end: int
            1-based inclusive

        strand: str
            '+' or '-'

        frame: int
            1, 2 or 3

        attributes: list of tuples of (key, val) pairs, where key is str and val is str/int/float
            [
                ('gene', 'dam'),
                ('locus_tag', 'T4p032')
                ('note', 'produces N6-methyladenine in GATC sites (in modified or non-modified cytosine DNA)'),
                ('codon_start', 1)
            ]

        tags: list of str

        regions: list of tuple of (start, end, strand) of each exon
            Default just one region

        partial_start: bool
            Partial 5' end

        partial_end: bool
            Partial 3' end

    """
    def __init__(self, seqname, type_, start, end, strand,
                 attributes=None, tags=None, regions=None, frame=1,
                 partial_start=False, partial_end=False):
        self.seqname = seqname
        self.type = type_
        self.start = start
        self.end = end
        self.strand = strand
        self.frame = frame
        self.partial_start = partial_start
        self.partial_end = partial_end

        if attributes is None:
            attributes = []
        self.attributes = attributes

        if tags is None:
            tags = []
        self.tags = tags

        if regions is None:
            regions = [(self.start, self.end, self.strand)]
        self.regions = regions

    def __len__(self):
        return self.end - self.start + 1

    def __repr__(self):
        ps = ['', ' (partial)'][self.partial_start]
        pe = ['', ' (partial)'][self.partial_end]

        attr_str = ''
        for key, val in self.attributes:
            if type(val) is str:
                attr_str += f"\n    {key}: '{val}'"
            else:  # type(val) is int or float
                attr_str += f"\n    {key}: {val}"

        text = f'''\
GenericFeature
  seqname: '{self.seqname}'
  type: '{self.type}'
  start: {self.start}{ps}
  end: {self.end}{pe}
  strand: '{self.strand}'
  frame: {self.frame}
  attributes: {attr_str}
  tags: {','.join(self.tags)}
  regions: {self.regions}'''

        return text

    def get_attribute(self, key):
        """
        Get the attribute value (i.e. content) with the key
        If more than one found, returns a list of values

        Args:
            key: str

        Returns: str, int, float, or list of str, int, float
        """
        vals = [v for k, v in self.attributes if k == key]
        if len(vals) == 0:
            return None
        elif len(vals) == 1:
            return vals[0]
        else:
            return vals

    def set_attribute(self, key, val):
        """
        Find the attribute with key and set the value
        If more than one attributes found, then set the first one, and remove the rest
        If no attribute found, then add an attribute with key, val

        Args:
            key: str

            val: str, int, or float
        """
        new = []  # new attributes list
        done = False  # done setting the attribute or not

        for k, v in self.attributes:
            if k == key:
                if not done:
                    new.append((key, val))
                    done = True
                else:
                    # Already done, don't append the (key, val)
                    #   to the new list, i.e. remove the attribute
                    pass
            else:
                # Keep existing attributes where k != key
                new.append((k, v))

        if not done:
            # No key found, add a new attribute
            new.append((key, val))

        self.attributes = new

    def add_attribute(self, key, val):
        """
        Add an attribute of (key, val)

        Args:
            key: str

            val: str, int, or float
        """
        self.attributes.append((key, val))

    def remove_attribute(self, key):
        """
        Remove all attributes with the key

        Args:
            key: str
        """
        self.attributes = [(k, v) for (k, v) in self.attributes if k != key]


class FeatureArray:
    """
    A list of GenericFeature that behaves like a list, but more than a list.

    self.__arr is the list storing GenericFeature objects

    Instance attributes:
        seqname: str
            The unique name of chromosome, genome or contig to which this feature_array belons

        genome_size: int (bp)

        features: list of GenericFeature or GtfFeature

        circular: bool
            Is circular genome or not
    """
    def __init__(self, seqname, genome_size, features=None, circular=False, sort=True):
        """
        Args:
            seqname: str

            genome_size: int

            features:
                Could be any of the following data types:
                    None, [],
                    GenericFeature, [GenericFeature, ...],
                    GtfFeature, [GtfFeature, ...]
                    GffFeature, [GffFeature, ...]

            circular: bool
                Circular molecule or not

            sort: bool
                Sort the input features or not
        """
        self.seqname = seqname
        self.genome_size = genome_size
        self.circular = circular
        self.__pos = 0

        if features is None:
            features = []
        elif features.__class__.__name__ in ['GenericFeature', 'GtfFeature', 'GffFeature']:
            features = [features]

        self.__arr = features

        # For each feature in the list, convert to GenericFeature
        for i, feature in enumerate(self.__arr):
            if feature.__class__.__name__ == 'GtfFeature':
                self.__arr[i] = gtf_to_generic_feature(feature)
            elif feature.__class__.__name__ == 'GffFeature':
                self.__arr[i] = gff_to_generic_feature(feature)

        if sort:
            self.sort()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__arr[item]
        elif isinstance(item, slice):
            return FeatureArray(
                seqname=self.seqname,
                genome_size=self.genome_size,
                features=self.__arr[item],
                circular=self.circular
            )
        else:
            raise TypeError('FeatureArray indices must be integers or slices')

    def __add__(self, other):
        if not other.__class__.__name__ == 'FeatureArray':
            raise TypeError(f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")

        for a in ['seqname', 'genome_size', 'circular']:
            assert getattr(self, a) == getattr(other, a)

        return FeatureArray(
            seqname=self.seqname,
            genome_size=self.genome_size,
            features=self.__arr + other.__arr,
            circular=self.circular,
            sort=False
        )

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos < len(self.__arr):
            r = self.__arr[self.__pos]
            self.__pos += 1
            return r
        else:
            self.__pos = 0
            raise StopIteration

    def __len__(self):
        return len(self.__arr)

    def __repr__(self):
        shape = ['linear', 'circular'][self.circular]
        text = f'''\
FeatureArray
  seqname: '{self.seqname}'
  genome size: {self.genome_size} bp ({shape})
  number of features: {len(self.__arr)}'''
        return text

    def __wrap(self):
        """
        For circular genomes the feature range can be out of bound (< 1 or > genome_size)
        This method wraps those positions back between 1..genome_size
        """
        size = self.genome_size
        for f in self.__arr:
            if f.start > size:
                f.start -= size
            elif f.start < 1:
                f.start += size

            if f.end > size:
                f.end -= size
            elif f.end < 1:
                f.end += size

            for i in range(len(f.regions)):
                start, end, strand = f.regions[i]

                if start > size:
                    start -= size
                elif start < 1:
                    start += size

                if end > size:
                    end -= size
                elif end < 1:
                    end += size

                f.regions[i] = (start, end, strand)

    def sort(self):
        """
        Sort the features in self.__arr by start positions
        """
        self.__arr = sorted(self.__arr, key=lambda f: f.start)

    def append(self, feature):
        """
        Append new GenericFeature. GtfFeature will be converted to GenericFeature
        """
        if feature.__class__.__name__ == 'GtfFeature':
            feature = gtf_to_generic_feature(feature)
        if feature.__class__.__name__ == 'GffFeature':
            feature = gff_to_generic_feature(feature)
        self.__arr.append(feature)

    def subset(self, start, end):
        """
        Subset (or filter) the features in self.__arr without changing their positions

        Args:
            start: int
                1-based, inclusive

            end: int
                1-based, inclusive
        """
        # Covers whole genome -> Do not subset
        if start == 1 and end == self.genome_size:
            return

        if not self.circular and end < start:
            raise AssertionError('For linear molecule end position must be greater or equal than start position')

        # Circular range -> Set end to greater than genome_size
        if end < start:
            end += self.genome_size

        arr = []
        for f in self.__arr:
            fs, fe = f.start, f.end
            # Circular feature -> Set feature end to greater than genome_size
            if fe < fs:
                fe += self.genome_size
            # Main criteria to be satisfied
            if start <= fs and fe <= end:
                arr.append(f)
        self.__arr = arr

    def offset(self, offset):
        """
        Offset (move) each feature in self.__arr

        Args:
            offset: int
        """
        size = self.genome_size
        for f in self.__arr:
            f.start += offset
            f.end += offset
            for i, region in enumerate(f.regions):
                start, end, strand = region
                start += offset
                end += offset
                f.regions[i] = (start, end, strand)

            if self.circular:
                self.__wrap()
            # After wrapping every feature will be in-bound

        in_bound = lambda x: 1 <= x.start <= size and 1 <= x.end <= size
        self.__arr = list(filter(in_bound, self.__arr))

    def crop(self, start, end):
        """
        Crop the features in self.__arr from <start> to <end>,
            which resets positions of features and the genome size

        Args:
            start: int
                1-based, inclusive

            end: int
                1-based, inclusive
        """
        # Covers whole genome -> Do not subset
        if start == 1 and end == self.genome_size:
            return

        if not self.circular and end < start:
            return

        self.subset(start, end)
        self.offset(-start + 1)
        self.genome_size = end - start + 1

    def reverse(self):
        """
        Reverse the features for reverse complementary of the genome sequence,
            which simply makes start as end, and end as start
        """
        size = self.genome_size
        for f in self.__arr:
            # Simultaneously update start and end
            f.start, f.end = (size - f.end + 1), (size - f.start + 1)
            f.strand = ['+', '-'][f.strand == '+']

            for i in range(len(f.regions)):
                start, end, strand = f.regions[i]
                # Simultaneously update start and end
                start, end = size - end + 1, size - start + 1
                strand = ['+', '-'][strand == '+']
                f.regions[i] = (start, end, strand)
            # Use start position to sort the regions (i.e. exons)
            f.regions = sorted(f.regions, key=lambda x: x[0])

        self.sort()

    def pop(self, index=-1):
        """
        Pop out a feature in the self.__arr
        """
        return self.__arr.pop(index)


class Chromosome:
    """
    An annotated chromosome

    Instance attributes:
        seqname: str
            The unique name of chromosome, genome or contig to which this feature_array belons

        sequence: str
            The genome sequence

        feature_array: FeatureArray object
            The annotation

        circular: bool
            Is circular genome or not

        genbank_LOCUS: str
            The complete LOCUS section of a genbank file
    """
    def __init__(self, seqname, sequence, feature_array, circular=False, genbank_LOCUS=''):
        self.seqname = seqname
        self.sequence = sequence
        self.feature_array = feature_array
        self.circular = circular
        self.genbank_LOCUS = genbank_LOCUS
