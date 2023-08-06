# This is the basic example of the README to get you started.
from genome_collector import GenomeCollection
import subprocess
collection = GenomeCollection()
db_path = collection.get_taxid_blastdb_path(taxid=511145, db_type='nucl')
process = subprocess.run([
    'blastn', '-db', db_path, '-query', 'queries.fa', '-out', 'results.txt'
])