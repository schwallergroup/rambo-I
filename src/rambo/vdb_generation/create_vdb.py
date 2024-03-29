import pandas as pd
import json
from rdkit import Chem
import openai
import sys
import os
import pkg_resources
import langchain
from langchain.cache import InMemoryCache
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import chromadb
from dotenv import load_dotenv

embedding_model = 'text-embedding-3-small'
save_path = './'

columns_to_keep = [
    "ReactionClass",
    "KeyWord_STD",
    "ReactionGroup",
    "RXN_SMILES",
    "PRODUCT_STRUCTURE",
    "Product_Yield_PCT_Area_UV",
    "Solvent_1_Name",
    "Reaction_T",
    "Reaction_Time_hrs",
    "Catalyst_1_eq",
    "catalyst_1_ID_1_SMILES",
    "catalyst_1_ID_2_SMILES",
    "Catalyst_1_Short_Hand",
    "Catalyst_2_eq",
    "catalyst_2_ID_1_SMILES",
    "catalyst_2_ID_2_SMILES",
    "Catalyst_2_Short_Hand",
    "Reactant_1_eq",
    "Reactant_1_SMILES",
    "Reactant_2_eq",
    "reactant_2_SMILES",
    "Reactant_3_eq",
    "reactant_3_SMILES",
    "Reagent_1_eq",
    "Reagent_1_Short_Hand",
    "Reagent_2_eq",
    "Reagent_2_Short_Hand"
]

def canonicalize_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        return Chem.MolToSmiles(mol, canonical=True)
    except:
        return None  
    
smiles_columns = [
    'PRODUCT_STRUCTURE',
    'catalyst_1_ID_1_SMILES',
    'catalyst_1_ID_2_SMILES',
    'catalyst_2_ID_1_SMILES',
    'catalyst_2_ID_2_SMILES',
    'Reactant_1_SMILES',
    'reactant_2_SMILES',
    'reactant_3_SMILES'
]

def create_text(row):
    text_parts = []
    text_parts.append(f"The reaction is classified under {row['ReactionClass']} with a standard keyword of {row['KeyWord_STD']}" if pd.notnull(row['ReactionClass']) and pd.notnull(row['KeyWord_STD']) else "")
    text_parts.append(f"and belongs to the {row['ReactionGroup']} group." if pd.notnull(row['ReactionGroup']) else "")
    text_parts.append(f"The reaction between {row['Reactant_1_SMILES']} (equivalent of {row['Reactant_1_eq']}) and {row['reactant_2_SMILES']} (equivalent of {row['Reactant_2_eq']})," if pd.notnull(row['Reactant_1_SMILES']) and pd.notnull(row['Reactant_1_eq']) and pd.notnull(row['reactant_2_SMILES']) and pd.notnull(row['Reactant_2_eq']) else "")
    text_parts.append(f"is catalyzed by {row['Catalyst_1_Short_Hand']} ([{row['catalyst_1_ID_1_SMILES']}, {row['catalyst_1_ID_2_SMILES']}], {row['Catalyst_1_eq']} equivalents)" if pd.notnull(row['Catalyst_1_Short_Hand']) and pd.notnull(row['catalyst_1_ID_1_SMILES']) and pd.notnull(row['catalyst_1_ID_2_SMILES']) and pd.notnull(row['Catalyst_1_eq']) else "")
    text_parts.append(f"and {row['Catalyst_2_Short_Hand']} ([{row['catalyst_2_ID_1_SMILES']}, {row['catalyst_2_ID_2_SMILES']}], {row['Catalyst_2_eq']} equivalents)," if pd.notnull(row['Catalyst_2_Short_Hand']) and pd.notnull(row['catalyst_2_ID_1_SMILES']) and pd.notnull(row['catalyst_2_ID_2_SMILES']) and pd.notnull(row['Catalyst_2_eq']) else "")
    text_parts.append(f"with {row['Solvent_1_Name']} as the solvent." if pd.notnull(row['Solvent_1_Name']) else "")
    text_parts.append(f"The reaction proceeds at {row['Reaction_T']}°C for {row['Reaction_Time_hrs']} hours." if pd.notnull(row['Reaction_T']) and pd.notnull(row['Reaction_Time_hrs']) else "")
    text_parts.append(f"The product obtained, {row['PRODUCT_STRUCTURE']}, has a structure represented by {row['RXN_SMILES']} for the reaction and {row['Product_Yield_PCT_Area_UV']}% yield as measured by UV area percent." if pd.notnull(row['PRODUCT_STRUCTURE']) and pd.notnull(row['RXN_SMILES']) and pd.notnull(row['Product_Yield_PCT_Area_UV']) else "")

    return ' '.join(filter(None, text_parts))

def create_reaction_details(row):

    reaction_details = {}

    def should_include(value):
        return not pd.isna(value) and value is not None

    if should_include(row.get('ReactionClass')):
        reaction_details['rxn_class'] = row['ReactionClass']
    if should_include(row.get('KeyWord_STD')):
        reaction_details['keyword'] = row['KeyWord_STD']
    if should_include(row.get('ReactionGroup')):
        reaction_details['reaction_group'] = row['ReactionGroup']


    reactants = [
        {"smiles": row['Reactant_1_SMILES'], "eq": row['Reactant_1_eq']} 
        for i in range(1, 3)  
        if should_include(row.get(f'Reactant_{i}_SMILES')) or should_include(row.get(f'Reactant_{i}_eq'))
    ]
    if reactants:
        reaction_details['reactants'] = reactants

    catalysts = []
    for i in range(1, 3):  
        catalyst = {
            "short_hand": row.get(f'Catalyst_{i}_Short_Hand'),
            "smiles": [
                row.get(f'catalyst_{i}_ID_1_SMILES'),
                row.get(f'catalyst_{i}_ID_2_SMILES')
            ],
            "eq": row.get(f'Catalyst_{i}_eq')
        }

        catalyst['smiles'] = [smile for smile in catalyst['smiles'] if should_include(smile)]
        if all(should_include(value) for key, value in catalyst.items() if key != 'smiles') or catalyst['smiles']:
            catalysts.append(catalyst)
    if catalysts:
        reaction_details['catalysts'] = catalysts

    if should_include(row.get('Solvent_1_Name')):
        reaction_details['solvent'] = row['Solvent_1_Name']
    if should_include(row.get('Reaction_T')):
        reaction_details['temperature'] = row['Reaction_T']
    if should_include(row.get('Reaction_Time_hrs')):
        reaction_details['time_hours'] = row['Reaction_Time_hrs']
    if should_include(row.get('PRODUCT_STRUCTURE')):
        reaction_details['product_structure'] = row['PRODUCT_STRUCTURE']
    if should_include(row.get('RXN_SMILES')):
        reaction_details['rxn_smiles'] = row['RXN_SMILES']
    if should_include(row.get('Product_Yield_PCT_Area_UV')):
        reaction_details['yield_pct'] = row['Product_Yield_PCT_Area_UV']

    return json.dumps(reaction_details)


def dict_to_text(reaction_details):
    text_representation = ""
    for key, value in reaction_details.items():
        if isinstance(value, list):
            for item in value:
                item_text = ", ".join([f"{k}: {v}" for k, v in item.items() if v is not None])
                text_representation += f"{key}: [{item_text}]\n"
        else:
            if value is not None:
                text_representation += f"{key}: {value}\n"
    return text_representation.strip()



class EmbeddingGenerator:
    @staticmethod
    def generate_embedding(chunk):
        global embedding_model
        try:
            response = openai.embeddings.create(
                input=chunk,
                model=embedding_model
            )
            embedding = response.data[0].embedding
            print("Embedding generated successfully.")
            return embedding
        except Exception as e:
            print(f"An error occurred while generating embedding: {e}")
            return None

class DataFrameManager:
    def __init__(self, save_path, text_column):
        global embedding_model
        self.embedding_generator = EmbeddingGenerator()
        self.chroma_client = chromadb.chromadb.PersistentClient(path=save_path)
        self.collection_name = f"{embedding_model}_{text_column}"
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name,
                                                                      metadata={"hnsw:space": "cosine"})
        
    def add_texts_to_collection(self, dataframe, text_column, columns_to_keep):
        embeddings_list = []
        documents_list = []
        metadatas_list = []
        ids_list = []
        
        for index, row in dataframe.iterrows():
            text = row[text_column]
            embedding = self.embedding_generator.generate_embedding(text)
            if embedding is not None:
                unique_id = f"row_{index}"
                embeddings_list.append(embedding)
                documents_list.append(text)

                metadata = {column: row[column] for column in columns_to_keep if row[column] is not None}
                
                metadatas_list.append(metadata)
                ids_list.append(unique_id)
        
        self.collection.add(
            embeddings=embeddings_list,
            documents=documents_list,
            metadatas=metadatas_list,
            ids=ids_list
        )
        return self.collection




if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    file_path = './data/8_SEPT_APPROVED_full_dataset.csv'
    df = pd.read_csv(file_path)
    df_filtered = df[columns_to_keep]
    for column in smiles_columns:
        df_filtered[column] = df_filtered[column].apply(canonicalize_smiles)
    df_filtered['text_description'] = df_filtered.apply(create_text, axis=1)
    df_filtered['dict_description'] = df_filtered.apply(create_reaction_details, axis=1)
    df_filtered = pd.read_csv(file_path)
    df_manager = DataFrameManager(save_path=save_path, text_column='text_description')
    collection = df_manager.add_texts_to_collection(df_filtered, text_column='text_description', columns_to_keep=columns_to_keep)
