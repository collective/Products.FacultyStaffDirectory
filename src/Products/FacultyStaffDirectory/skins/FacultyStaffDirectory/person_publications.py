
# Return all publications of the current 'FSDPerson' context based
# on a simple match of the persons's name against the author list.
# a Person object. The heuristic is pretty lame right now.


def normalize(s):
    s = s.lower()
    s = s.replace('ue', 'u')
    s = s.replace('ae', 'a')
    s = s.replace('oe', 'o')
    s = s.replace('ü', 'u')
    s = s.replace('ä', 'a')
    s = s.replace('ö', 'o')
    s = s.replace('&auml;', 'a')
    s = s.replace('&ouml;', 'o')
    s = s.replace('&uuml;', 'u')
    return s


if not context.portal_type == 'FSDPerson':
    raise TypeError('context object must be instance of FSDPerson')

# search all bib references first
fsd = context.getDirectoryRoot()
fsd_path = '/'.join(fsd.getPhysicalPath())
reference_types =   context.portal_bibliography.getReferenceTypes()

# Filter by author name 
firstname = context.getFirstName().strip()
lastname = context.getLastName().strip()

# Filter 1: the author names are indexed using 'SearchableText'.
# So figure out all documents where the first and last name are
# fulltext indexed
stext = ' AND '.join([item.strip() for item in (firstname, lastname) if item.strip()])
results = context.portal_catalog(path=fsd_path,
                                 SearchableText=stext,
                                 meta_type=reference_types)


# sort by year desc
sort_on = [('publication_year', 'cmp', 'desc')]
results = sequence.sort(results, sort_on)

# Filter 2: really check if the lastname of the person can be found
# within the list of authors

results2 = list()
lastname = normalize(context.getLastName().strip())

for r in results:
    # This check is lame!
    authors = normalize(r.Authors)
    if lastname in authors:
        results2.append(r)

return [r.getObject() for r in results2]
