from py2neo import Graph, Node, Relationship, NodeMatcher


class GraphUtils():

    def __init__(self, graph):
        self.graph = graph


    def paragraphs_for_filename(self, filename):
        kwargs = { "filename": filename }
        cypher = """
            MATCH(paragraph :p {filename:{filename}})-[:FACS]->(zone :zone)
            RETURN paragraph
        """
        cursor = self.graph.run(
            cypher,
            parameters = {
                "filename": filename
            }
        )

        paragraphs = []
        while cursor.forward():
            for paragraph in cursor.current:
                paragraphs.append(paragraph)

        return paragraphs

    def nodes_with_link_for_filename(self, filename):
        """for a given filename, this query returns all nodes
        that contain any of the link_attributes (see below)
        The goal is to create relationships from these nodes to their targets
        """

        kwargs = { "filename": filename }
        link_attributes = ["facs", "next", "prev", "target", "ref"]
        where = " OR ".join("EXISTS(n.{})".format(attr) for attr in link_attributes)
        cypher = """
            MATCH (n)
            WHERE 
        """
        cypher += where
        cypher += " RETURN n"

        nodes = []
        while cursor.forward():
            for nodes in cursor.current:
                nodes.append(nodes)

        return nodes


    def concatenation_exists(self, node):
        cypher = """
        MATCH (node1)-[r :CONCATENATED]->(node2)
        WHERE ID(node1) = {node_id}
        RETURN r
        """
        cursor = self.graph.run(cypher, parameters={"node_id": node.identity})

        # return 1 if there exists a relation
        return cursor.forward()


    def tokens_in_paragraph(self, paragraph:Node, concatenated=0):
        """For a given paragraph, this method returns all nodes
        connected via a NEXT relationship. 
        If concatenated=1, it will return a concatenated version of the textpath.
        Returns all nodes in the found textpath.
        """

        cypher="""
        MATCH (para)-[:NEXT]->(t),
        textpath = shortestPath((t)-[:NEXT*]->(lt))
        WHERE ID(para)={paragraph_id}
        AND (para)-[:LAST]->(lt)
        AND ALL (
            rel IN relationships(textpath)
            WHERE (rel.concatenated IS NULL OR rel.concatenated = {concatenated})
        )
        RETURN nodes(textpath)
        """
        # NOTE: it is assumed that a path containing a concatenated (non-hyphened)
        # word will be always shorter than a path containing a hyphened word.
        # The non-concatenated textpath actually never has the relation-attribute 
        # rel.concatenated=0 (it is always NULL)

        cursor = self.graph.run(
            cypher, 
            parameters={
                "paragraph_id": paragraph.identity,
                "concatenated": concatenated
            }
        ) 

        nodes = [] 
        while cursor.forward():
            for entry in cursor.current:
                for node in entry:
                    nodes.append(node)
                
        return nodes


    def create_unhyphenated(self, tokens):
        """tokens=Array of all tokens in a paragraph, as returned
        by GraphUtils.tokens_in_paragraph(para). This procedures looks for linebreaks with type=hyph
        If found, it looks forward and backwards to find the hyphened wordparts
        It then concatenates the wordparts, creates a new Node and new Releations.
        """
        tx = self.graph.begin()

        for i, token in enumerate(tokens):
            j=0
            k=0
            if token.has_label('lb'):
                wordstart = None
                wordend = None
                if token.get('type') == 'hyph':
                    
                    # walk back and find a token which is a wordpart
                    # and not any punctuation or similar
                    j=i-1
                    while j>0:
                        #print("j = {}".format(j))
                        if tokens[j].has_label('token') \
                        and tokens[j]["string"] \
                        and not tokens[j]["is_punct"]: 
                            #print("TRY: "+str(tokens[j]))
                            wordstart = tokens[j]
                            break
                        else:
                            j = j-1

                    # walk forward and find a token
                    k=i+1
                    while k>0 and tokens[k]:
                        #print("k = {}".format(k))
                        if tokens[k].has_label('token'):
                            #print("TRY END: "+str(tokens[k]))
                            wordend = tokens[k]
                            break
                        else:
                            k = k+1
                          
                    concat_word = ''
                    if wordstart and wordend and not self.concatenation_exists(wordstart):
                        #print("---START: "+str(wordstart))
                        #print("---  END: "+str(wordend))
                        if any(
                            wordstart["string"].endswith(s) for s\
                            in ['-', '\N{NOT SIGN}', '\N{NON-BREAKING HYPHEN}']
                        ):
                            concat_word = wordstart["string"][:-1]
                        else:
                            concat_word = wordstart["string"]
                            
                        concat_word += wordend["string"]
                        
                        # create new concatenated token
                        # with blank as whitespace
                        labels = list(
                            set(
                                ['token', 'concatenated'] + list(wordstart.labels) + list(wordend.labels)
                            )
                        )
                        attrs = { 
                            "string"    : concat_word,
                            "whitespace": wordend["whitespace"],
                            "filename"  : wordstart["filename"],
                            "idno"      : wordstart["idno"],
                        }
                        concat_node = Node(
                            *labels,
                            **attrs
                        )
                        #print("+ {}".format(concat_word))
                        tx.create(concat_node)
                        
                        # create relations from hyphened wordpards to concatenated word
                        rs = Relationship(
                            wordstart,
                            "CONCATENATED",
                            concat_node
                        )
                        rs2 = Relationship(
                            wordend,
                            "CONCATENATED",
                            concat_node
                        )
                        tx.create(rs)                
                        tx.create(rs2)
                        
                        # create direct connection for non-hyphened version
                        # of the thext
                        if j >0:
                            before_wordstart = tokens[j-1]
                            rs3 = Relationship(
                                before_wordstart,
                                "NEXT",
                                concat_node,
                                concatenated=1
                            )
                            tx.create(rs3)
                            
                        if len(tokens) > k+1:
                            after_wordend = tokens[k+1]
                            rs4 = Relationship(
                                concat_node,
                                "NEXT",
                                after_wordend,
                                concatenated=1
                            )
                            tx.create(rs4)

        tx.commit()


    def link_inner_relationships(self, filename):
        """creates new relationships between nodes of a given filename,
        that contain one of the link attributes below which point to
        a node inside the same xml file.

        Within a link attribute, pointers can be separated by whitespace
        https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.global.linking.html

        This method should be only run once after a TEI document has
        been parsed.
        """
        
        link_attributes = ["facs", "next", "prev", "target", "ref"]

        cypher = """
	MATCH (from_node)
	WHERE from_node.filename = "{filename}"
	    AND EXISTS(from_node.{link_attribute})
	WITH from_node, SPLIT(from_node.{link_attribute}, " ") AS pointers
	UNWIND pointers as pointer
	WITH from_node, SPLIT(pointer, "#") AS target
        WITH from_node, target, CASE WHEN target[0] = "" THEN "{filename}" ELSE target[0] END AS filename
	MATCH (to_node)
	    WHERE to_node.`xml:id` = target[1]
	    AND to_node.filename = filename
	CREATE (from_node)-[r:{relation_name}]->(to_node)
        """

        for link_attribute in link_attributes:
            parameters = {
                "filename"      : filename,
                "link_attribute": link_attribute,
                "relation_name" : link_attribute.upper(),
            }
            cursor = self.graph.run(cypher.format(**parameters))

        #create_links = True
        #for label in labels:
        #    if label in elements_not_to_link:
        #        create_links = False

        #if create_links:
        #    for link_attribute in link_attributes:
        #        if link_attribute in attrs:
        #            print(link_attribute)
        #            for link in attrs[link_attribute].split():
        #                (filename, xml_id) = link.split("#")

        #                if not filename:
        #                    filename = attrs['filename']
        #                if not filename:
        #                    raise ValueError("filename not found in attribute: {}".format(link_attribute))
        #                if not xml_id:
        #                    raise ValueError("xml:id not found in attribute: {}".format(link_attribute))

        #                ex_node = None
        #                if filename in node_cache and xml_id in node_cache[filename]:
        #                    ex_node = node_cache[filename][xml_id]

        #                if not ex_node:
        #                    print("NODE {} {} does not exist: search in db".format(filename, xml_id))
        #                    # try to find that node in the database instead
        #                    search_attrs = {}
        #                    search_attrs['filename'] = filename
        #                    search_attrs['xml:id'] = xml_id
        #                    ex_node = matcher.match(**search_attrs).first()
        #                else:
        #                    print("NODE {} {} exists in cache".format(filename, xml_id))

        #                if ex_node:
        #                    print("NODE {} {} create RLS".format(filename, xml_id))
        #                    # we found an existing node:
        #                    # create a relationship to that existing node
        #                    rs = Relationship(
        #                        node,
        #                        link_attribute,
        #                        ex_node
        #                    )
        #                    tx.create(rs)
        #                else:
        #                    print("NODE {} {} does not exist: create empty node".format(filename, xml_id))
        #                    # we only got a reference to a node, but not the node itself:
        #                    # create an «empty» ref_node and a relation to it:
        #                    ref_node = Node(**search_attrs)
        #                    tx.create(ref_node)
        #                    # store the reference node in the node_cache as well,
        #                    # there might be more than one reference to it
        #                    if not filename in node_cache:
        #                        node_cache[filename] = {}
        #                    node_cache[filename][xml_id] = ref_node
        #                    
        #                    rs = Relationship(
        #                        node,
        #                        link_attribute,
        #                        ref_node
        #                    )
        #                    tx.create(rs)
