from sqlmodel import Session, select

from app.db.database import get_engine
from app.db.init_db import init_database
from app.modules.activity_logs.activity_model import ActivityLog
from app.modules.archive_entries.archive_entry_model import ArchiveEntry
from app.modules.personal_ratings.rating_model import Rating


# ---------------------------------------------------------------------------
# Seed data — archive entries
# ---------------------------------------------------------------------------

ARCHIVE_ENTRIES_SEED = [
    {
        "title": "Resident Evil",
        "alias_title": "Biohazard",
        "release_year": 1996,
        "main_protagonist": "Jill Valentine / Chris Redfield",
        "original_platform": "PlayStation",
        "registered_platforms": "PlayStation, Saturn, PC, Nintendo DS, GameCube",
        "chronology_order": 1,
        "chronology_era": "Classic Era",
        "description": (
            "The game that started it all. S.T.A.R.S. Alpha Team investigates the Spencer "
            "Mansion after contact with Bravo Team is lost. Inside, they discover the "
            "horrifying results of Umbrella's illegal T-Virus research program."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "high",
        "director": "Shinji Mikami",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "Custom Engine (PS1)",
        "umbrella_classification": "Spencer Mansion Incident",
        "survival_index": 62,
        "players": 1,
        "estimated_duration": 480,
        "main_locations": "Spencer Mansion, Raccoon Forest, Underground Laboratory",
        "threat_type": "T-Virus Bioweapons (Zombies, Hunters, Cerberus)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 2",
        "alias_title": "Biohazard 2",
        "release_year": 1998,
        "main_protagonist": "Leon S. Kennedy / Claire Redfield",
        "original_platform": "PlayStation",
        "registered_platforms": "PlayStation, PC, N64, GameCube, Dreamcast",
        "chronology_order": 2,
        "chronology_era": "Classic Era",
        "description": (
            "Two months after the Spencer Mansion incident, Raccoon City is overrun by a "
            "T-Virus outbreak. Rookie cop Leon Kennedy and college student Claire Redfield "
            "fight to survive and uncover Umbrella's darkest secrets beneath the city."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Hideki Kamiya",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "Custom Engine (PS1)",
        "umbrella_classification": "Raccoon City Incident",
        "survival_index": 48,
        "players": 1,
        "estimated_duration": 600,
        "main_locations": "Raccoon City Streets, Police Department, Umbrella Laboratory",
        "threat_type": "T-Virus, G-Virus (G-Mutants, Tyrant T-103)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 3: Nemesis",
        "alias_title": "Biohazard 3: Last Escape",
        "release_year": 1999,
        "main_protagonist": "Jill Valentine",
        "original_platform": "PlayStation",
        "registered_platforms": "PlayStation, PC, GameCube, Dreamcast",
        "chronology_order": 3,
        "chronology_era": "Classic Era",
        "description": (
            "Set around the events of RE2, Jill Valentine attempts to escape Raccoon City "
            "while being relentlessly hunted by Nemesis-T — an advanced Umbrella "
            "Bio-Organic Weapon programmed to eliminate all S.T.A.R.S. members."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Kazuhiro Aoyama",
        "developer": "Capcom",
        "genre": "Survival Horror / Action",
        "engine_name": "Custom Engine (PS1)",
        "umbrella_classification": "Raccoon City Incident / Nemesis Program",
        "survival_index": 52,
        "players": 1,
        "estimated_duration": 420,
        "main_locations": "Raccoon City, Clock Tower, Hospital, Dead Factory",
        "threat_type": "Nemesis-T Type, T-Virus Bioweapons",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil Code: Veronica",
        "alias_title": "Biohazard Code: Veronica",
        "release_year": 2000,
        "main_protagonist": "Claire Redfield / Chris Redfield",
        "original_platform": "Dreamcast",
        "registered_platforms": "Dreamcast, PlayStation 2, GameCube, PlayStation 3, Xbox 360",
        "chronology_order": 4,
        "chronology_era": "Classic Era",
        "description": (
            "After escaping Raccoon City, Claire is captured by Umbrella and imprisoned "
            "on Rockfort Island. When a T-Virus outbreak strikes, she must survive "
            "alongside the enigmatic Alexia Ashford, keeper of the deadly Veronica virus."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Hiroki Kato",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "Custom Engine (DC/PS2)",
        "umbrella_classification": "Rockfort Island Incident / Veronica Virus Program",
        "survival_index": 45,
        "players": 1,
        "estimated_duration": 720,
        "main_locations": "Rockfort Island, Antarctic Facility",
        "threat_type": "T-Virus, Veronica Virus (Alexia Ashford)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 0",
        "alias_title": "Biohazard 0",
        "release_year": 2002,
        "main_protagonist": "Rebecca Chambers / Billy Coen",
        "original_platform": "GameCube",
        "registered_platforms": "GameCube, Wii, PC, PlayStation 3, Xbox 360, PlayStation 4, Xbox One",
        "chronology_order": 5,
        "chronology_era": "Classic Era",
        "description": (
            "A prequel set hours before the Spencer Mansion incident. S.T.A.R.S. medic "
            "Rebecca Chambers and escaped convict Billy Coen are stranded at a deserted "
            "Umbrella training facility overrun by experimental BOWs, uncovering the "
            "true origins of the T-Virus outbreak."
        ),
        "category": "prequel",
        "status": "registered",
        "threat_level": "high",
        "director": "Koji Oda",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "Custom Engine (GCN)",
        "umbrella_classification": "Arklay Mountains Incident / Zero Program",
        "survival_index": 58,
        "players": 1,
        "estimated_duration": 540,
        "main_locations": "Ecliptic Express, Umbrella Training Facility, Marcus Laboratory",
        "threat_type": "T-Virus, Leech BOWs (James Marcus Reanimation)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil Remake",
        "alias_title": "Biohazard / Resident Evil HD",
        "release_year": 2002,
        "main_protagonist": "Jill Valentine / Chris Redfield",
        "original_platform": "GameCube",
        "registered_platforms": "GameCube, Wii, PC, PlayStation 3, Xbox 360, PlayStation 4, Xbox One",
        "chronology_order": 6,
        "chronology_era": "Classic Era",
        "description": (
            "A faithful yet massively expanded reimagining of the 1996 original, featuring "
            "redesigned environments, new enemies, deeper lore and the terrifying Crimson "
            "Heads mechanic. Widely regarded as one of the greatest survival horror games "
            "ever made."
        ),
        "category": "remake",
        "status": "registered",
        "threat_level": "high",
        "director": "Shinji Mikami",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "Custom Engine (GCN)",
        "umbrella_classification": "Spencer Mansion Incident (Classified Reconstruction)",
        "survival_index": 68,
        "players": 1,
        "estimated_duration": 540,
        "main_locations": "Spencer Mansion, Guardhouse, Underground Laboratory",
        "threat_type": "T-Virus Bioweapons (Crimson Heads, Hunters, Tyrant T-002)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 4",
        "alias_title": "Biohazard 4",
        "release_year": 2005,
        "main_protagonist": "Leon S. Kennedy",
        "original_platform": "GameCube",
        "registered_platforms": "GameCube, PlayStation 2, PC, Wii, iOS, PlayStation 3, Xbox 360, PlayStation 4, Xbox One, Nintendo Switch",
        "chronology_order": 7,
        "chronology_era": "Modern Era",
        "description": (
            "Leon S. Kennedy is sent to rural Spain to rescue the U.S. President's "
            "daughter from a mysterious cult. Abandoning fixed cameras, RE4 revolutionized "
            "the series and the third-person shooter genre with its over-the-shoulder "
            "perspective and relentless pacing."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Shinji Mikami",
        "developer": "Capcom",
        "genre": "Survival Horror / Third-Person Shooter",
        "engine_name": "Custom Engine (GCN)",
        "umbrella_classification": "Los Illuminados Incident / Plaga Parasite Program",
        "survival_index": 72,
        "players": 1,
        "estimated_duration": 960,
        "main_locations": "Rural Village, Lake, Castle Salazar, Military Island",
        "threat_type": "Plaga Parasites (Ganados, El Gigante, Regeneradors)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 5",
        "alias_title": "Biohazard 5",
        "release_year": 2009,
        "main_protagonist": "Chris Redfield / Sheva Alomar",
        "original_platform": "PlayStation 3",
        "registered_platforms": "PlayStation 3, Xbox 360, PC, PlayStation 4, Xbox One, Nintendo Switch",
        "chronology_order": 8,
        "chronology_era": "Modern Era",
        "description": (
            "BSAA agents Chris Redfield and Sheva Alomar investigate bioterrorism "
            "in the Kijuju region of Africa, discovering a massive Majini infection "
            "and the return of a familiar nemesis wielding an evolved strain of the "
            "Uroboros virus."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Jun Takeuchi",
        "developer": "Capcom",
        "genre": "Survival Horror / Third-Person Shooter",
        "engine_name": "MT Framework",
        "umbrella_classification": "Kijuju Incident / Uroboros Program",
        "survival_index": 65,
        "players": 2,
        "estimated_duration": 840,
        "main_locations": "Kijuju, Ancient Ruins, Tricell Facility",
        "threat_type": "Plaga Parasites, Uroboros Virus (Albert Wesker)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 6",
        "alias_title": "Biohazard 6",
        "release_year": 2012,
        "main_protagonist": "Leon S. Kennedy / Chris Redfield / Jake Muller",
        "original_platform": "PlayStation 3",
        "registered_platforms": "PlayStation 3, Xbox 360, PC, PlayStation 4, Xbox One, Nintendo Switch",
        "chronology_order": 9,
        "chronology_era": "Modern Era",
        "description": (
            "The most ambitious entry in the series, with three interlocking campaigns. "
            "Leon battles a C-Virus outbreak in Tall Oaks, Chris confronts bioterrorism "
            "in Eastern Europe, and Jake Muller carries the key to the antivirus in "
            "his own blood."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Hiroyuki Kobayashi",
        "developer": "Capcom",
        "genre": "Third-Person Shooter / Survival Horror",
        "engine_name": "MT Framework",
        "umbrella_classification": "Global Bioterrorism Incident / C-Virus Program",
        "survival_index": 70,
        "players": 2,
        "estimated_duration": 1440,
        "main_locations": "Tall Oaks, Lanshiang, Eastern Europe, Underwater Facility",
        "threat_type": "C-Virus (J'avo, Chrysalid, Carla Radames)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 7: Biohazard",
        "alias_title": "Biohazard 7: Resident Evil",
        "release_year": 2017,
        "main_protagonist": "Ethan Winters",
        "original_platform": "PlayStation 4",
        "registered_platforms": "PlayStation 4, Xbox One, PC, Nintendo Switch, PlayStation 5, Xbox Series X/S",
        "chronology_order": 10,
        "chronology_era": "New Era",
        "description": (
            "A bold reimagining of the series in first-person. Ethan Winters searches "
            "for his missing wife at a decrepit Louisiana plantation, where the infected "
            "Baker family and the mysterious Eveline hold terrifying secrets tied to "
            "a new bioweapon."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Koshi Nakanishi",
        "developer": "Capcom",
        "genre": "Survival Horror / First-Person",
        "engine_name": "RE Engine",
        "umbrella_classification": "Baker Incident / Mold (Eveline Program)",
        "survival_index": 55,
        "players": 1,
        "estimated_duration": 600,
        "main_locations": "Baker Plantation, Guest House, Salt Mines, Wrecked Ship",
        "threat_type": "Mold / Eveline (Molded, Marguerite, Jack Baker)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 2 Remake",
        "alias_title": "Biohazard RE:2",
        "release_year": 2019,
        "main_protagonist": "Leon S. Kennedy / Claire Redfield",
        "original_platform": "PlayStation 4",
        "registered_platforms": "PlayStation 4, Xbox One, PC, PlayStation 5, Xbox Series X/S",
        "chronology_order": 11,
        "chronology_era": "Classic Era",
        "description": (
            "A stunning modern reimagining of the 1998 classic. Leon and Claire's "
            "escape from Raccoon City is retold with over-the-shoulder gameplay, "
            "masterfully redesigned environments and the relentless Mr. X tracking "
            "every corridor of the RPD."
        ),
        "category": "remake",
        "status": "registered",
        "threat_level": "critical",
        "director": "Kazunori Kadoi",
        "developer": "Capcom",
        "genre": "Survival Horror / Third-Person",
        "engine_name": "RE Engine",
        "umbrella_classification": "Raccoon City Incident (Classified Reconstruction)",
        "survival_index": 50,
        "players": 1,
        "estimated_duration": 720,
        "main_locations": "Raccoon City, RPD, Sewers, Underground Laboratory",
        "threat_type": "T-Virus, G-Virus (Mr. X, G-William Birkin)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 3 Remake",
        "alias_title": "Biohazard RE:3",
        "release_year": 2020,
        "main_protagonist": "Jill Valentine",
        "original_platform": "PlayStation 4",
        "registered_platforms": "PlayStation 4, Xbox One, PC, PlayStation 5, Xbox Series X/S",
        "chronology_order": 12,
        "chronology_era": "Classic Era",
        "description": (
            "Jill Valentine's escape from Raccoon City is reimagined with modern graphics "
            "and gameplay. A visually spectacular Nemesis adapts and evolves while hunting "
            "Jill across an infected city as she races to synthesize a vaccine against "
            "the T-Virus."
        ),
        "category": "remake",
        "status": "registered",
        "threat_level": "critical",
        "director": "Masachika Kawata",
        "developer": "Capcom",
        "genre": "Survival Horror / Action",
        "engine_name": "RE Engine",
        "umbrella_classification": "Raccoon City Incident / Nemesis Program (Classified Reconstruction)",
        "survival_index": 60,
        "players": 1,
        "estimated_duration": 420,
        "main_locations": "Raccoon City, Hospital, Dead Factory, NEST 2",
        "threat_type": "Nemesis (NE-α Parasite Type), T-Virus Bioweapons",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil Village",
        "alias_title": "Biohazard Village / Resident Evil 8",
        "release_year": 2021,
        "main_protagonist": "Ethan Winters",
        "original_platform": "PlayStation 4",
        "registered_platforms": "PlayStation 4, PlayStation 5, Xbox One, Xbox Series X/S, PC",
        "chronology_order": 13,
        "chronology_era": "New Era",
        "description": (
            "Three years after the Baker incident, Ethan Winters and his family are "
            "targeted in a remote European village by a mysterious cult led by Mother "
            "Miranda. Ethan must traverse a landscape of gothic horror across four "
            "distinct lords to rescue his daughter Rose."
        ),
        "category": "main_series",
        "status": "registered",
        "threat_level": "critical",
        "director": "Morimasa Sato",
        "developer": "Capcom",
        "genre": "Survival Horror / First-Person",
        "engine_name": "RE Engine",
        "umbrella_classification": "European Village Incident / Cadou Parasite Program",
        "survival_index": 62,
        "players": 1,
        "estimated_duration": 720,
        "main_locations": "Dimitrescu Castle, Moreau Reservoir, Heisenberg Factory, Beneviento Estate",
        "threat_type": "Cadou Parasite / Mold (Lady Dimitrescu, Heisenberg, Mother Miranda)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil 4 Remake",
        "alias_title": "Biohazard RE:4",
        "release_year": 2023,
        "main_protagonist": "Leon S. Kennedy",
        "original_platform": "PlayStation 4",
        "registered_platforms": "PlayStation 4, PlayStation 5, Xbox Series X/S, PC",
        "chronology_order": 14,
        "chronology_era": "Modern Era",
        "description": (
            "A definitive reimagining of the landmark 2005 original. Features fully "
            "rebuilt environments, expanded lore, a more nuanced Ashley Graham and "
            "modernized combat that honors the spirit of the original while surpassing "
            "it in scope, tension and emotional depth."
        ),
        "category": "remake",
        "status": "registered",
        "threat_level": "critical",
        "director": "Yasuhiro Anpo",
        "developer": "Capcom",
        "genre": "Survival Horror / Third-Person Shooter",
        "engine_name": "RE Engine",
        "umbrella_classification": "Los Illuminados Incident (Classified Reconstruction)",
        "survival_index": 75,
        "players": 1,
        "estimated_duration": 960,
        "main_locations": "Rural Village, Lake, Castle Salazar, Military Island",
        "threat_type": "Plaga Parasites (Ganados, Blind Zealots, Regeneradors, Krauser)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil Revelations",
        "alias_title": "Biohazard Revelations",
        "release_year": 2012,
        "main_protagonist": "Jill Valentine / Chris Redfield",
        "original_platform": "Nintendo 3DS",
        "registered_platforms": "Nintendo 3DS, PC, PlayStation 3, Xbox 360, Wii U, PlayStation 4, Xbox One, Nintendo Switch",
        "chronology_order": 15,
        "chronology_era": "Modern Era",
        "description": (
            "Set between RE4 and RE5, Jill Valentine and her partner Parker Luciani are "
            "trapped aboard the abandoned ocean liner Queen Zenobia, while Chris Redfield "
            "investigates a BSAA operation gone dark. A claustrophobic return to "
            "survival horror tension."
        ),
        "category": "spin_off",
        "status": "registered",
        "threat_level": "high",
        "director": "Eiichiro Sasaki",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "MT Framework",
        "umbrella_classification": "Queen Zenobia Incident / T-Abyss Virus Program",
        "survival_index": 60,
        "players": 2,
        "estimated_duration": 600,
        "main_locations": "Queen Zenobia, Mediterranean Sea, Terragrigia",
        "threat_type": "T-Abyss Virus (Ooze, Scarmiglione, Sea Creepers)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
    {
        "title": "Resident Evil Revelations 2",
        "alias_title": "Biohazard Revelations 2",
        "release_year": 2015,
        "main_protagonist": "Claire Redfield / Barry Burton",
        "original_platform": "PlayStation 3",
        "registered_platforms": "PlayStation 3, PlayStation 4, Xbox 360, Xbox One, PC, PlayStation Vita, Nintendo Switch",
        "chronology_order": 16,
        "chronology_era": "Modern Era",
        "description": (
            "Claire Redfield and Moira Burton are abducted and imprisoned on a remote "
            "island facility. Months later, Barry Burton searches for his daughter "
            "accompanied by the mysterious Natalia. An episodic survival horror with "
            "dual-protagonist gameplay and a branching narrative."
        ),
        "category": "spin_off",
        "status": "registered",
        "threat_level": "high",
        "director": "Michiteru Okabe",
        "developer": "Capcom",
        "genre": "Survival Horror",
        "engine_name": "MT Framework",
        "umbrella_classification": "Isolation Island Incident / Uroboros / Iota Virus",
        "survival_index": 58,
        "players": 2,
        "estimated_duration": 720,
        "main_locations": "Detention Facility, Village, Sewers, Tower",
        "threat_type": "Uroboros variants, Iota Virus (Afflicted, Glasps, Neil Fisher)",
        "cover_image_url": None,
        "cover_image_public_id": None,
    },
]


# ---------------------------------------------------------------------------
# Seed data — ratings
# ---------------------------------------------------------------------------

RATINGS_SEED = [
    {
        "title": "Resident Evil",
        "score": 8.0,
        "review": (
            "The origin of survival horror. Dated mechanics met with brilliance in "
            "level design and atmosphere. A landmark achievement that holds up decades later."
        ),
    },
    {
        "title": "Resident Evil 2",
        "score": 8.5,
        "review": (
            "A masterpiece of narrative pacing and dual-storyline design. Raccoon City "
            "feels alive and the parallel campaigns remain among the finest in the series."
        ),
    },
    {
        "title": "Resident Evil 3: Nemesis",
        "score": 7.8,
        "review": (
            "Nemesis as a concept is iconic and the tension of being pursued is relentless. "
            "Shorter than RE2 and more linear, but delivers on spectacle and atmosphere."
        ),
    },
    {
        "title": "Resident Evil Code: Veronica",
        "score": 7.5,
        "review": (
            "An ambitious but uneven entry. Alexia Ashford is a compelling villain and "
            "the Antarctic setting is memorable, though pacing issues and item management "
            "frustrate at times."
        ),
    },
    {
        "title": "Resident Evil 0",
        "score": 8.2,
        "review": (
            "A polished prequel with a clever partner system and exceptional atmosphere. "
            "The Umbrella training facility is among the most memorable locations in the "
            "classic era of the franchise."
        ),
    },
    {
        "title": "Resident Evil Remake",
        "score": 8.8,
        "review": (
            "The definitive version of the original. Crimson Heads add genuine terror, "
            "the expanded lore is impeccable, and the production quality was extraordinary "
            "for its time. A masterclass in remake craftsmanship."
        ),
    },
    {
        "title": "Resident Evil 4",
        "score": 9.5,
        "review": (
            "A revolutionary masterpiece that reinvented both the franchise and the "
            "action game genre. Nearly two decades later, its design remains unmatched "
            "in pacing, invention and moment-to-moment satisfaction."
        ),
    },
    {
        "title": "Resident Evil 5",
        "score": 8.0,
        "review": (
            "A spectacular co-op experience with tight gunplay and a strong narrative "
            "conclusion to the Wesker arc. Less frightening than its predecessors but "
            "immensely satisfying as an action title."
        ),
    },
    {
        "title": "Resident Evil 6",
        "score": 8.5,
        "review": (
            "Ambitious and divisive. The scale of three interlocking campaigns is "
            "genuinely impressive, and Leon's chapter is a highlight of the modern era. "
            "A flawed but memorable achievement in scope."
        ),
    },
    {
        "title": "Resident Evil 7: Biohazard",
        "score": 8.5,
        "review": (
            "A brilliant return to survival horror roots. The first-person perspective "
            "is expertly executed and the Baker family are among the most memorable "
            "antagonists the franchise has ever produced."
        ),
    },
    {
        "title": "Resident Evil 2 Remake",
        "score": 9.3,
        "review": (
            "An outstanding reimagining that surpasses the original in nearly every "
            "dimension. Mr. X's relentless pursuit and the beautifully realized RPD "
            "make this an essential experience."
        ),
    },
    {
        "title": "Resident Evil 3 Remake",
        "score": 7.5,
        "review": (
            "Technically impressive but narratively condensed. The reimagined Nemesis "
            "is a visual spectacle, though the shorter runtime and condensed scope "
            "disappoint fans of the original."
        ),
    },
    {
        "title": "Resident Evil Village",
        "score": 8.9,
        "review": (
            "An exhilarating evolution of RE7's formula. Lady Dimitrescu and Heisenberg "
            "are unforgettable creations. The gothic variety of the village districts "
            "makes for the most diverse and visually striking entry in years."
        ),
    },
    {
        "title": "Resident Evil 4 Remake",
        "score": 9.6,
        "review": (
            "A landmark remake that elevates the source material in every dimension. "
            "The expanded world, modernized combat and emotional depth make this the "
            "definitive version of an all-time classic and one of the finest games "
            "of its generation."
        ),
    },
    {
        "title": "Resident Evil Revelations",
        "score": 7.5,
        "review": (
            "A claustrophobic gem born from handheld constraints. The Queen Zenobia "
            "setting is genuinely unsettling and the episodic structure keeps tension "
            "high, though the story meanders in its second half."
        ),
    },
    {
        "title": "Resident Evil Revelations 2",
        "score": 7.8,
        "review": (
            "A surprising highlight of the spin-off line. Barry and Natalia's chapters "
            "are emotionally resonant and the episodic format creates effective "
            "cliffhanger tension across its four episodes."
        ),
    },
]


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

def seed_archive_entries(session: Session) -> tuple[dict[str, ArchiveEntry], int]:
    """Insert archive entries not yet in the DB. Returns a title→entry map and insert count."""
    entries_by_title: dict[str, ArchiveEntry] = {}
    inserted = 0

    for data in ARCHIVE_ENTRIES_SEED:
        existing = session.exec(
            select(ArchiveEntry).where(ArchiveEntry.title == data["title"])
        ).first()

        if existing:
            entries_by_title[data["title"]] = existing
        else:
            entry = ArchiveEntry(**data)
            session.add(entry)
            entries_by_title[data["title"]] = entry
            inserted += 1

    return entries_by_title, inserted


def seed_ratings(session: Session, entries_by_title: dict[str, ArchiveEntry]) -> int:
    """Insert ratings for entries that don't yet have one. Returns insert count."""
    inserted = 0

    for item in RATINGS_SEED:
        entry = entries_by_title.get(item["title"])
        if entry is None or entry.id is None:
            continue

        existing = session.exec(
            select(Rating).where(Rating.series_id == entry.id)
        ).first()

        if existing:
            continue

        session.add(Rating(
            series_id=entry.id,
            score=item["score"],
            review=item["review"],
        ))
        inserted += 1

    return inserted


def seed_activity_logs(session: Session, entries_by_title: dict[str, ArchiveEntry]) -> int:
    """Insert game_created and rating_created logs, plus a single global archive_sync."""
    inserted = 0

    # One game_created log per archive entry
    for title, entry in entries_by_title.items():
        if entry.id is None:
            continue

        exists = session.exec(
            select(ActivityLog)
            .where(ActivityLog.series_id == entry.id)
            .where(ActivityLog.action == "game_created")
        ).first()

        if not exists:
            session.add(ActivityLog(
                series_id=entry.id,
                action="game_created",
                message=f"Archive entry '{title}' registered in Umbrella Records.",
                new_value=title,
            ))
            inserted += 1

    # One rating_created log per seeded rating
    for item in RATINGS_SEED:
        entry = entries_by_title.get(item["title"])
        if entry is None or entry.id is None:
            continue

        exists = session.exec(
            select(ActivityLog)
            .where(ActivityLog.series_id == entry.id)
            .where(ActivityLog.action == "rating_created")
        ).first()

        if not exists:
            session.add(ActivityLog(
                series_id=entry.id,
                action="rating_created",
                message=(
                    f"Initial rating of {item['score']}/10 recorded "
                    f"for '{item['title']}'."
                ),
                new_value=str(item["score"]),
            ))
            inserted += 1

    # One global archive_sync log with series_id = NULL
    sync_exists = session.exec(
        select(ActivityLog)
        .where(ActivityLog.action == "archive_sync")
        .where(ActivityLog.series_id.is_(None))  # type: ignore[union-attr]
    ).first()

    if not sync_exists:
        session.add(ActivityLog(
            series_id=None,
            action="archive_sync",
            message="Initial seed of the Umbrella Records archive completed. 16 entries loaded.",
        ))
        inserted += 1

    return inserted


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def seed_database() -> None:
    """Initialize the database and insert all seed data idempotently."""
    init_database()

    with Session(get_engine()) as session:
        entries_by_title, entries_count = seed_archive_entries(session)
        # flush to populate auto-generated IDs before ratings/logs reference them
        session.flush()

        ratings_count = seed_ratings(session, entries_by_title)
        logs_count = seed_activity_logs(session, entries_by_title)

        session.commit()

    print("Seed completed.")
    print(f"  Archive entries inserted: {entries_count}")
    print(f"  Ratings inserted:         {ratings_count}")
    print(f"  Activity logs inserted:   {logs_count}")


def main() -> None:
    seed_database()


if __name__ == "__main__":
    main()
