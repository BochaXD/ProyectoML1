def _get_nodes(self):
        node1, node2 = ast.parse(self._code1), ast.parse(self._code2)
        return node1, node2         