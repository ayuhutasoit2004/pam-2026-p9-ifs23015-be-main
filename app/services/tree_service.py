from app.extensions import SessionLocal
from app.models.tree import Tree
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_tree_response, parse_identify_response


def generate_tree_info(name: str):
    session = SessionLocal()
    try:
        prompt = f"""
        Dalam format JSON, berikan informasi lengkap tentang pohon "{name}".
        Format:
        {{
            "name": "nama pohon",
            "description": "deskripsi lengkap pohon",
            "facts": "fakta-fakta menarik tentang pohon",
            "benefits": "manfaat pohon bagi lingkungan dan manusia"
        }}
        Jawab hanya dengan JSON, tanpa penjelasan tambahan.
        """

        result = generate_from_llm(prompt)
        data = parse_tree_response(result)

        tree = Tree(
            name=data.get("name", name),
            description=data.get("description", ""),
            facts=data.get("facts", ""),
            benefits=data.get("benefits", ""),
            type="generate"
        )
        session.add(tree)
        session.commit()
        session.refresh(tree)

        return {
            "id": tree.id,
            "name": tree.name,
            "description": tree.description,
            "facts": tree.facts,
            "benefits": tree.benefits,
            "type": tree.type,
            "created_at": tree.created_at.isoformat()
        }

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def identify_tree(characteristics: str):
    session = SessionLocal()
    try:
        prompt = f"""
        Dalam format JSON, identifikasi jenis pohon berdasarkan ciri-ciri berikut: "{characteristics}".
        Format:
        {{
            "name": "nama pohon yang paling mungkin",
            "description": "penjelasan mengapa pohon ini sesuai dengan ciri-ciri tersebut",
            "facts": "fakta-fakta menarik tentang pohon ini",
            "benefits": "manfaat pohon ini"
        }}
        Jawab hanya dengan JSON, tanpa penjelasan tambahan.
        """

        result = generate_from_llm(prompt)
        data = parse_identify_response(result)

        tree = Tree(
            name=data.get("name", "Unknown"),
            description=data.get("description", ""),
            facts=data.get("facts", ""),
            benefits=data.get("benefits", ""),
            type="identify"
        )
        session.add(tree)
        session.commit()
        session.refresh(tree)

        return {
            "id": tree.id,
            "name": tree.name,
            "description": tree.description,
            "facts": tree.facts,
            "benefits": tree.benefits,
            "type": tree.type,
            "created_at": tree.created_at.isoformat()
        }

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_trees(page: int = 1, per_page: int = 10, type_filter: str = None):
    session = SessionLocal()
    try:
        query = session.query(Tree)

        if type_filter:
            query = query.filter(Tree.type == type_filter)

        total = query.count()

        data = (
            query
            .order_by(Tree.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "facts": t.facts,
                "benefits": t.benefits,
                "type": t.type,
                "created_at": t.created_at.isoformat()
            }
            for t in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }
    finally:
        session.close()


def delete_tree(tree_id: int):
    session = SessionLocal()
    try:
        tree = session.query(Tree).filter(Tree.id == tree_id).first()
        if not tree:
            return False
        session.delete(tree)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
