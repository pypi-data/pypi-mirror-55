import abc
import json
from typing import Union, Mapping, TypeVar, Tuple, Dict, List, Type, Generic, Optional, Callable, Any

# noinspection Mypy
from pydgraph import DgraphClient
from grapl_analyzerlib.nodes.types import PropertyT, OneOrMany, Property

T = TypeVar("T")

EdgeViewT = Union[List[Type["Viewable[T]"]], Type["Viewable[T]"]]

class Viewable(abc.ABC, Generic[T]):

    dynamic_forward_edge_types = {}  # type: Dict[str, EdgeViewT[T]]
    dynamic_reverse_edge_types = {}  # type: Dict[str, Tuple[EdgeViewT[T], str]]
    dynamic_property_types = {}  # type: Dict[str, PropertyT]

    def __init__(
        self: "Viewable[T]", dgraph_client: DgraphClient, node_key: str, uid: str,
            **args: Any
    ) -> None:
        self.dgraph_client = dgraph_client
        self.node_key = node_key
        self.uid = uid

        self.dynamic_forward_edges = {}  # type: Dict[str, 'ForwardEdgeView[T]']
        self.dynamic_reverse_edges = {}  # type: Dict[str,  'ReverseEdgeView[T]']
        self.dynamic_properties = {}  # type: Dict[str, Property]

    @staticmethod
    @abc.abstractmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        pass

    @staticmethod
    @abc.abstractmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT[T]"]:
        pass

    @staticmethod
    @abc.abstractmethod
    def _get_reverse_edge_types() -> Mapping[str, Tuple["EdgeViewT[T]", str]]:
        """
        :return: Mapping of reverse edge name to Tuple of edge type and forward edge name
        """
        pass

    @abc.abstractmethod
    def _get_properties(self) -> Mapping[str, 'Property']:
        pass

    @abc.abstractmethod
    def _get_forward_edges(self) -> 'Mapping[str, ForwardEdgeView[T]]':
        pass

    @abc.abstractmethod
    def _get_reverse_edges(self) -> 'Mapping[str,  ReverseEdgeView[T]]':
        pass

    @classmethod
    def get_edge_types(cls) -> Mapping[str, Union["EdgeViewT[T]", Tuple["EdgeViewT[T]", str]]]:
        return {
            **cls._get_forward_edge_types(),
            **cls.dynamic_forward_edge_types,
            **cls.dynamic_reverse_edge_types,
            **cls._get_reverse_edge_types()
        }

    def set_dynamic_property_type(self, prop_name: str, prop_type: "PropertyT") -> None:
        self.dynamic_property_types[prop_name] = prop_type

    @classmethod
    def set_dynamic_forward_edge_type(
        cls, edge_name: str, edge_type: "EdgeViewT[T]"
    ) -> None:
        cls.dynamic_forward_edge_types[edge_name] = edge_type

    def set_dynamic_reverse_edge_type(
        self, edge_name: str, edge_type: "EdgeViewT[T]", forward_name: str
    ) -> None:
        self.dynamic_reverse_edge_types[edge_name] = edge_type, forward_name

    def set_dynamic_property(self, prop_name: str, prop: "Property") -> None:
        self.dynamic_properties[prop_name] = prop

    def set_dynamic_forward_edge(
            self, edge_name: str, edge: 'ForwardEdgeView[T]'
    ) -> None:
        if edge:
            self.dynamic_forward_edges[edge_name] = edge

    def set_dynamic_reverse_edge(
            self, edge_name: str, reverse_edge:  'ReverseEdgeView[T]'
    ) -> None:
        self.dynamic_reverse_edges[edge_name] = reverse_edge

    def get_properties(self) -> Mapping[str, 'Property']:
        return {
            **self._get_properties(),
            **self.dynamic_properties,
            'node_key': self.node_key,
            'uid': self.uid,
        }

    def get_forward_edges(self) -> 'Mapping[str, ForwardEdgeView[T]]':
        return {k: v for k, v in {**self._get_forward_edges(), **self.dynamic_forward_edges}.items() if v}

    def get_reverse_edges(self) -> 'Mapping[str,  ReverseEdgeView[T]]':
        return {k: v for k, v in {**self._get_reverse_edges(), **self.dynamic_reverse_edges}.items() if v[0]}

    def get_edges(self) -> 'Mapping[str, EdgeView[T]]':
        return {**self.get_forward_edges(), **self.get_reverse_edges()}

    def fetch_property(
            self, prop_name: str, prop_type: Callable[['Property'], 'Property']
    ) -> Optional[Union[str, int]]:
        node_key_prop = ""
        if prop_name != "node_key":
            node_key_prop = "node_key"
        query = f"""
            {{
                res(func: uid("{self.uid}"), first: 1) @cascade {{
                    uid,
                    {node_key_prop},
                    {prop_name}
                }}
            
            }}
        """

        txn = self.dgraph_client.txn(read_only=True)
        try:
            res = json.loads(txn.query(query).json)
        finally:
            txn.discard()
        raw_prop = res["res"]
        if raw_prop is None:
            return None

        if raw_prop[0].get(prop_name) is None:
            return None

        prop = prop_type(raw_prop[0][prop_name])

        return prop

    def fetch_properties(
            self, prop_name: str, prop_type: Callable[['Property'], 'Property']
    ) -> List['Property']:
        query = f"""
            {{
                res(func: uid("{self.uid}")) @cascade {{
                    uid,
                    node_key,
                    {prop_name}
                }}
            
            }}
        """
        txn = self.dgraph_client.txn(read_only=True)
        try:
            res = json.loads(txn.query(query).json)
        finally:
            txn.discard()
        raw_props = res["res"]

        if not raw_props:
            return []

        props = [prop_type(p[prop_name]) for p in raw_props]

        return props

    def fetch_edge(self, edge_name: str, edge_type: Type['Viewable[T]']) -> Optional['Viewable[T]']:
        query = f"""
            {{
                res(func: uid("{self.uid}"), first: 1) {{
                    uid,
                    node_key,
                    {edge_name} {{
                        uid,
                        node_type,
                        node_key,
                    }}
                }}
            
            }}
        """

        txn = self.dgraph_client.txn(read_only=True)
        try:
            res = json.loads(txn.query(query).json)
        finally:
            txn.discard()

        raw_edge = res["res"]
        if not raw_edge or not raw_edge[0].get(edge_name):
            return None

        edge = edge_type.from_dict(self.dgraph_client, raw_edge[0][edge_name][0])  # type: Viewable[T]
        return edge

    def fetch_edges(self, edge_name: str, edge_type: Type['Viewable[T]']) -> List['Viewable[T]']:
        query = f"""
            {{
                res(func: uid("{self.uid}")) {{
                    uid,
                    node_key,
                    {edge_name} {{
                        uid,
                        node_type,
                        node_key,
                    }}
                }}
            
            }}
        """
        txn = self.dgraph_client.txn(read_only=True)
        try:
            res = json.loads(txn.query(query).json)
        finally:
            txn.discard()

        raw_edges = res["res"]

        if not raw_edges or not raw_edges[0].get(edge_name):
            return []

        raw_edges = raw_edges[0][edge_name]
        edges = [edge_type.from_dict(self.dgraph_client, f) for f in raw_edges]  # type: List[Viewable[T]]

        return edges

    @classmethod
    def from_dict(cls: Type['Viewable[T]'], dgraph_client: DgraphClient, d: Dict[str, Any]) -> 'Viewable[T]':
        properties = {}
        if d.get("node_type"):
            properties["node_type"] = d["node_type"]

        for prop, into in cls._get_property_types().items():
            val = d.get(prop)

            if val or val == 0:
                if into == str:
                    val = str(val)
                elif into == int:
                    val = int(val)
                properties[prop] = val

        edges = {}  # type: Dict[str, Union[Viewable[T], List[Viewable[T]]]]
        for edge_tuple in cls.get_edge_types().items():
            edge_name = edge_tuple[0]  # type: str
            forward_name = None  # type: Optional[str]
            if isinstance(edge_tuple[1], tuple):
                ty = edge_tuple[1][0]  # type: EdgeViewT[T]
                forward_name = edge_tuple[1][1]
            else:
                ty = edge_tuple[1]

            raw_edge = d.get(edge_name, None)

            if not raw_edge:
                continue

            if isinstance(ty, List):
                ty = ty[0]

                if d.get(edge_name, None):
                    f_edge = d[edge_name]
                    if isinstance(f_edge, list):
                        _edges = [ty.from_dict(dgraph_client, f) for f in f_edge]
                    elif isinstance(f_edge, dict):
                        _edges = [ty.from_dict(dgraph_client, f_edge)]
                    else:
                        raise TypeError(f'Edge {edge_name} must be list or dict')

                    if forward_name:
                        edges[forward_name] = _edges
                    else:
                        edges[edge_name] = _edges

            else:
                if isinstance(raw_edge, list):
                    edge = ty.from_dict(dgraph_client, raw_edge[0])
                elif isinstance(raw_edge, dict):
                    edge = ty.from_dict(dgraph_client, raw_edge)
                else:
                    raise TypeError(f'Edge {edge_name} must be list or dict')


                if forward_name:
                    edges[forward_name] = edge
                else:
                    edges[edge_name] = edge

        cleaned_edges = {}  # type: Dict[str, Union[Viewable[T], List[Viewable[T]]]]
        for _edge in edges.items():
            edge_name = _edge[0]
            cleaned_edge = _edge[1]  # type: Union[Viewable[T], List[Viewable[T]]]
            if edge_name[0] == "~":
                edge_name = edge_name[1:]
            cleaned_edges[edge_name] = cleaned_edge

        return cls(
            dgraph_client=dgraph_client,
            node_key=d["node_key"],
            uid=d["uid"],
            **properties,
            **cleaned_edges,
        )

    def to_dict(self) -> Dict[str, Any]:
        node_dict = dict(self.get_properties())
        node_dict["node_key"] = self.node_key
        edges = []

        for edge_name, edge in self.get_edges().items():
            # List of forward edges
            if isinstance(edge, list):
                for e in edge:
                    edges.append(
                        {"from": self.node_key, "edge_name": edge_name, "to": e.node_key}
                    )
            # One or Many reverse edges
            elif isinstance(edge, tuple):
                # Many reverse edges
                if isinstance(edge[0], list):
                    for e in edge[0]:
                        edges.append(
                            {"from": self.node_key, "edge_name": edge_name, "to": e.node_key}
                        )
                # One reverse edge
                else:
                    edges.append(
                        {"from": edge[0].node_key, "edge_name": edge_name, "to": edge[0].node_key}
                    )
            # One forward edge
            else:
                edges.append(
                    {"from": edge.node_key, "edge_name": edge_name, "to": edge.node_key}
                )

        return {"node": node_dict, "edges": edges}


ForwardEdgeView = OneOrMany['Viewable[T]']
ReverseEdgeView = Tuple[OneOrMany['Viewable[T]'], str]
EdgeView = Union['ForwardEdgeView[T]', 'ReverseEdgeView[T]']

