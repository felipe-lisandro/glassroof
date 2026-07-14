from datetime import date, datetime, timedelta, timezone

from app import create_app, db
from app.models.avaliation import Avaliation
from app.models.category import Category
from app.models.image import Image
from app.models.location import Location
from app.models.property import Property
from app.models.user import EnterpriseUser, PersonUser
from app.models.visit import Visit


def reset_database() -> None:
    # Recreate schema from scratch to keep model and DB in sync.
    db.drop_all()
    db.create_all()


def create_users() -> tuple[list[EnterpriseUser], list[PersonUser]]:
    enterprises_data = [
        {
            "name": "Horizonte Imoveis",
            "email": "contato@horizonte.com",
            "cnpj": "12.345.678/0001-90",
            "raw_password": "senha123",
        },
        {
            "name": "VivaLar Empreendimentos",
            "email": "comercial@vivalar.com",
            "cnpj": "23.456.789/0001-01",
            "raw_password": "senha123",
        },
        {
            "name": "NovaCasa Prime",
            "email": "atendimento@novacasa.com",
            "cnpj": "34.567.890/0001-12",
            "raw_password": "senha123",
        },
        {
            "name": "Alvo Imobiliaria",
            "email": "suporte@alvoimobiliaria.com",
            "cnpj": "45.678.901/0001-23",
            "raw_password": "senha123",
        },
    ]

    people_data = [
        {
            "name": "Ana",
            "last_name": "Silva",
            "email": "ana.silva@email.com",
            "cpf": "123.456.789-00",
            "birthday": date(1995, 5, 17),
            "raw_password": "senha123",
        },
        {
            "name": "Bruno",
            "last_name": "Costa",
            "email": "bruno.costa@email.com",
            "cpf": "234.567.890-11",
            "birthday": date(1992, 8, 4),
            "raw_password": "senha123",
        },
        {
            "name": "Carla",
            "last_name": "Oliveira",
            "email": "carla.oliveira@email.com",
            "cpf": "345.678.901-22",
            "birthday": date(1998, 11, 29),
            "raw_password": "senha123",
        },
        {
            "name": "Diego",
            "last_name": "Souza",
            "email": "diego.souza@email.com",
            "cpf": "456.789.012-33",
            "birthday": date(1990, 2, 10),
            "raw_password": "senha123",
        },
    ]

    enterprises: list[EnterpriseUser] = []
    for item in enterprises_data:
        enterprise = EnterpriseUser(
            name=item["name"],
            email=item["email"],
            cnpj=item["cnpj"],
        )
        enterprise.set_password(item["raw_password"])
        enterprises.append(enterprise)

    people: list[PersonUser] = []
    for item in people_data:
        person = PersonUser(
            name=item["name"],
            last_name=item["last_name"],
            email=item["email"],
            cpf=item["cpf"],
            birthday=item["birthday"],
        )
        person.set_password(item["raw_password"])
        people.append(person)

    db.session.add_all(enterprises + people)
    db.session.commit()
    return enterprises, people


def create_properties(enterprises: list[EnterpriseUser]) -> list[Property]:
    properties_data = [
        {
            "name": "Apartamento Solar",
            "description": "Apartamento de 2 quartos com varanda e boa iluminacao.",
            "price": 380000.0,
            "enterprise_id": enterprises[0].id,
            "overall_rating": 4.4,
        },
        {
            "name": "Casa Jardim Azul",
            "description": "Casa ampla com quintal e area gourmet.",
            "price": 620000.0,
            "enterprise_id": enterprises[1].id,
            "overall_rating": 4.2,
        },
        {
            "name": "Studio Centro",
            "description": "Studio moderno proximo a transporte publico.",
            "price": 290000.0,
            "enterprise_id": enterprises[2].id,
            "overall_rating": 4.0,
        },
        {
            "name": "Cobertura Vista Verde",
            "description": "Cobertura com vista panoramica e 3 suites.",
            "price": 950000.0,
            "enterprise_id": enterprises[3].id,
            "overall_rating": 4.8,
        },
    ]

    properties = [Property(**item) for item in properties_data]
    db.session.add_all(properties)
    db.session.commit()
    return properties


def create_locations(properties: list[Property]) -> None:
    locations_data = [
        {
            "street": "Rua das Flores",
            "number": 101,
            "CEP": "13050-100",
            "complement": "Apto 12",
            "city": "Campinas",
            "state": "SP",
            "country": "Brasil",
            "property_id": properties[0].id,
        },
        {
            "street": "Avenida Central",
            "number": 222,
            "CEP": "13050-200",
            "complement": "Casa",
            "city": "Campinas",
            "state": "SP",
            "country": "Brasil",
            "property_id": properties[1].id,
        },
        {
            "street": "Rua do Comercio",
            "number": 55,
            "CEP": "13050-300",
            "complement": "Studio 304",
            "city": "Campinas",
            "state": "SP",
            "country": "Brasil",
            "property_id": properties[2].id,
        },
        {
            "street": "Alameda das Araucarias",
            "number": 780,
            "CEP": "13050-400",
            "complement": "Cobertura 2",
            "city": "Campinas",
            "state": "SP",
            "country": "Brasil",
            "property_id": properties[3].id,
        },
    ]

    db.session.add_all([Location(**item) for item in locations_data])
    db.session.commit()


def create_images(properties: list[Property]) -> None:
    images_data = [
        {
            "URL": "https://picsum.photos/id/1011/800/600",
            "size_mb": 2,
            "order": 1,
            "description": "Fachada principal",
            "property_id": properties[0].id,
        },
        {
            "URL": "https://picsum.photos/id/1025/800/600",
            "size_mb": 3,
            "order": 1,
            "description": "Quintal e jardim",
            "property_id": properties[1].id,
        },
        {
            "URL": "https://picsum.photos/id/1031/800/600",
            "size_mb": 2,
            "order": 1,
            "description": "Sala integrada",
            "property_id": properties[2].id,
        },
        {
            "URL": "https://picsum.photos/id/1043/800/600",
            "size_mb": 4,
            "order": 1,
            "description": "Varanda gourmet",
            "property_id": properties[3].id,
        },
    ]

    db.session.add_all([Image(**item) for item in images_data])
    db.session.commit()


def create_categories() -> dict[str, Category]:
    categories_data = [
        {
            "name": "Vizinhanca",
            "description": "Percepcao sobre seguranca, ruido e convivio local.",
        },
        {
            "name": "Localizacao",
            "description": "Acesso a transporte, servicos e pontos da cidade.",
        },
        {
            "name": "Infraestrutura",
            "description": "Qualidade estrutural do imovel e areas comuns.",
        },
        {
            "name": "Preco",
            "description": "Relacao custo-beneficio percebida pelo usuario.",
        },
        {
            "name": "Experiencia com locatario",
            "description": "Qualidade da relacao e suporte durante a locacao.",
        },
    ]

    categories = [Category(**item) for item in categories_data]
    db.session.add_all(categories)
    db.session.commit()
    return {item.name: item for item in categories}


def create_avaliations(
    properties: list[Property],
    categories_by_name: dict[str, Category],
    people: list[PersonUser],
) -> None:
    comments = {
        0: [
            ("Vizinhanca", "Rua silenciosa e com boa iluminacao publica.", 5),
            ("Preco", "Valor competitivo para a regiao.", 4),
            ("Infraestrutura", "Predio bem cuidado e com manutencao em dia.", 5),
        ],
        1: [
            ("Experiencia com locatario", "Atendimento rapido e transparente.", 5),
            ("Localizacao", "Mercado e farmacia bem proximos.", 4),
            ("Preco", "Um pouco acima da media do bairro.", 3),
        ],
        2: [
            ("Localizacao", "Excelente para quem trabalha no centro.", 5),
            ("Infraestrutura", "Espaco interno compacto, mas funcional.", 4),
            ("Vizinhanca", "Movimento moderado em horario comercial.", 4),
        ],
        3: [
            ("Infraestrutura", "Acabamento premium em todos os ambientes.", 5),
            ("Preco", "Preco elevado, porem condizente com a entrega.", 4),
            ("Experiencia com locatario", "Negociacao clara e sem atrasos.", 5),
        ],
    }

    avaliations: list[Avaliation] = []
    for index, prop in enumerate(properties):
        user = people[index % len(people)]
        for position, (category_name, comment, stars) in enumerate(comments[index]):
            category = categories_by_name[category_name]
            avaliations.append(
                Avaliation(
                    property_id=prop.id,
                    user_id=user.id,
                    category_id=category.id,
                    comment=comment,
                    stars=stars,
                    created_at=datetime.now(timezone.utc) - timedelta(days=position + index),
                    photos=[f"https://picsum.photos/seed/{prop.id}-{position}/600/400"],
                )
            )

    db.session.add_all(avaliations)
    db.session.commit()


def create_visits(properties: list[Property], people: list[PersonUser]) -> None:
    base_time = datetime.now(timezone.utc) + timedelta(days=1)
    visits_data = [
        {
            "property_id": properties[0].id,
            "user_id": people[0].id,
            "scheduled_at": base_time,
            "status": "pending",
            "note": "Primeira visita do casal.",
        },
        {
            "property_id": properties[1].id,
            "user_id": people[1].id,
            "scheduled_at": base_time + timedelta(days=1),
            "status": "confirmed",
            "note": "Interesse em financiamento.",
        },
        {
            "property_id": properties[2].id,
            "user_id": people[2].id,
            "scheduled_at": base_time + timedelta(days=2),
            "status": "pending",
            "note": "Cliente precisa de vaga de garagem.",
        },
        {
            "property_id": properties[3].id,
            "user_id": people[3].id,
            "scheduled_at": base_time + timedelta(days=3),
            "status": "cancelled",
            "note": "Remarcacao solicitada.",
        },
    ]

    db.session.add_all([Visit(**item) for item in visits_data])
    db.session.commit()


def seed() -> None:
    app = create_app()
    with app.app_context():
        reset_database()
        enterprises, people = create_users()
        properties = create_properties(enterprises)
        create_locations(properties)
        create_images(properties)
        categories_by_name = create_categories()
        create_avaliations(properties, categories_by_name, people)
        create_visits(properties, people)

        print("Seed concluido com sucesso.")
        print("- 4 empresas e 4 pessoas cadastradas")
        print("- 4 imoveis cadastrados")
        print("- 4 localizacoes e 4 imagens")
        print("- 5 categorias globais cadastradas")
        print("- 12 avaliacoes (3 por imovel, com category_id e user_id)")
        print("- 4 visitas cadastradas")


if __name__ == "__main__":
    seed()
