"""
Test connector item.
"""

from gaphor import UML
from gaphor.diagram.components.connector import ConnectorItem
from gaphor.tests.testcase import TestCase


class ConnectorItemTestCase(TestCase):
    """
    Connector item basic tests.
    """

    def test_create(self):
        """Test creation of connector item
        """
        conn = self.create(ConnectorItem, UML.Connector)
        assert not conn.subject is None
        # self.assertTrue(conn.end is None)

    def test_persistence(self):
        """Test connector item saving/loading
        """
        conn = self.create(ConnectorItem, UML.Connector)

        end = self.element_factory.create(UML.ConnectorEnd)
        # conn.end = end

        data = self.save()
        assert end.id in data

        self.load(data)

        connectors = self.diagram.canvas.select(lambda e: isinstance(e, ConnectorItem))
        ends = self.kindof(UML.ConnectorEnd)
