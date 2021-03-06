#!/usr/bin/env python
#
# Copyright (C) 2018 Vanessa Sochat.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This scrips will produce a massive summary tree (and save to file, if 
# argument is provided

# We expect to have a pickled tree as first argument (being used in container)
import pickle
import json
import time
import sys
import os

database = '/code/database.pkl'
if not os.path.exists(database):
    print('Database not found at %s' %database)
    sys.exit(1)

print('Loading Saved Container Tree:')
tree = pickle.load(open(database, 'rb'))

# Do the comparison with the rest
containers = tree.root.tags

print('%s of containers are found in tree!' %len(containers)) 

score_matrix = []

# Now we can generate a little matrix of similarity scores!
print('Calculating (non optimized) score matrix!')
for container1 in containers:
    score_row = []
    for container2 in containers:
        tags = [container1, container2]
        result = tree.similarity_score(tags)
        score_row.append(result['score'])        
    score_matrix.append(score_row)

# Create temporary directory and copy file there
from containertree.utils import get_template
from containertree.server import serve_template
import shutil
import tempfile

# Copy the file to the webroot
webroot = tempfile.mkdtemp()
print('Webroot: %s' %webroot)
template = get_template('heatmap')
shutil.copyfile(template, "%s/index.html" %webroot)

# Generate the data.json
print('Exporting data for d3 visualization')
data = {"data": score_matrix, "X": containers, "Y": containers}
with open('%s/data.json' %webroot, 'w') as filey:
    filey.writelines(json.dumps(data))

serve_template(webroot, port=9779)
