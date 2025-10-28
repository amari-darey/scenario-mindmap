import json
from PyQt6.QtGui import QColor
from core.node import NodeItem
from core.edge import EdgeItem

class JSONStorage:
    @staticmethod
    def save(path, scene):
        data = {'nodes': [], 'edges': []}
        nodes = [it for it in scene.items() if isinstance(it, NodeItem)]
        for n in nodes:
            data['nodes'].append(n.to_dict())
        edges = [it for it in scene.items() if isinstance(it, EdgeItem)]
        for e in edges:
            data['edges'].append(e.to_dict())
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(path, scene, create_node_fn, create_edge_fn):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for it in list(scene.items()):
            scene.removeItem(it)
        id_map = {}
        for nd in data.get('nodes', []):
            color = QColor(*nd.get('color', [255,255,200]))
            pos_x = nd.get('x', 0)
            pos_y = nd.get('y', 0)
            node = create_node_fn(nd.get('text', 'Node'), pos=(pos_x, pos_y), color=color, uid=nd.get('id'),
                                  note=nd.get('note', ''), font_family=nd.get('font_family'), font_size=nd.get('font_size'))
            id_map[nd.get('id')] = node
        for ed in data.get('edges', []):
            parent = id_map.get(ed.get('source'))
            child = id_map.get(ed.get('dest'))
            if parent and child:
                create_edge_fn(scene, parent, child)
