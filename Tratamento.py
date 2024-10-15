import pandas as pd
import streamlit as st
import openpyxl



st.set_page_config(page_title="Itinerario",
                   page_icon=":bar_chart:",
                   layout="wide")


#--------------------------------------comando de cache e carregamento---------------------
#criar opção de upload e de cache
#criar def importação de it e cache
def carregar_itinerarios():
    itinerario1 = pd.read_excel(upload_file, engine="openpyxl")
    return itinerario1


#criar def contadores leitura remota de it e cache
def carregar_contador():
    contador1 = pd.read_excel(upload_file, engine="openpyxl")
    return contador1


#criar def leitura remota e cache
#criar def contadores leitura remota de it e cache
def carregar_remota():
    remota1 = pd.read_excel(upload_file, engine="openpyxl")
    return remota1


#---------------------------------------importação e tratamento-----------------------------
st.subheader("Importação de Itinerarios e Leitura Remota")

# importar itinerarios
upload_file = st.file_uploader("Importar Itinerarios", type="xlsx")
if upload_file:
    st.markdown("---")
    itinerario = carregar_itinerarios()
    itinerario.head()

    #definir codigo a serem convertidos na função do aparelho
    dados = [
        ["11", "Ativa"],
        ["12", "Ativa"],
        ["21", "Agua"],
        ["41", "Ativa"],
        ["49", "Reativa"],
        ["61", "Ativa"],
        ["69", "Reativa"],
        ["71", "Ponta"],
    ]
    fun = pd.DataFrame(dados, columns=['Função', 'Descrição'])
    # converter na função a coluna para formato inteiro
    fun['Função'] = fun['Função'].astype(int)
    fun.head()

    # alterar codigo de função para descrição do codigo
    itfun = pd.merge(itinerario, fun, on='Função', how='left')
    itfun.head()

    # definir roteiro qual unidade comercial usar
    dados = [["Avenças PRAIA", "Praia"],
             ["GC REMOTA", "Praia"],
             ["IP PRAIA REMOTA", "Praia"],
             ["IP PRAIA", "Praia"],
             ["MT", "Praia"],
             ["Praia GC I", "Praia"],
             ["Praia GC II", "Praia"],
             ["Praia GC III", "Praia"],
             ["Praia", "Praia"],
             ["Rural", "Praia"],
             ["ADS - S.Domingos", "São.Domingos"],
             ["Avenças S.DOMINGOS", "São.Domingos"],
             ["MT S.DOMINGOS", "São.Domingos"],
             ["Milho Branco", "São.Domingos"],
             ["Praia Baixo e Praia Formosa", "São.Domingos"],
             ["Roteiro IP S.DOMINGOS REMOTA", "São.Domingos"],
             ["S.DOMINGOS GC", "São.Domingos"],
             ["S.DOMINGOS", "São.Domingos"],
             ["ADS - Assomada", "Santa Catarina"],
             ["Assomada", "Santa Catarina"],
             ["GC Santa Catarina", "Santa Catarina"],
             ["Picos", "Santa Catarina"],
             ["Roteiro IP Santa Catarina", "Santa Catarina"],
             ["Rª da Barca", "Santa Catarina"],
             ["ADS - Tarrafal", "Tarrafal"],
             ["Roteiro IP TARRAFAL", "Tarrafal"],
             ["Tarrafal - CHÃO BOM", "Tarrafal"],
             ["Tarrafal - VILA", "Tarrafal"],
             ["Tarrafal", "Tarrafal-Rural"],
             ["ADS - Calheta", "Calheta"],
             ["CALHETA I", "Calheta"],
             ["CALHETA II", "Calheta"],
             ["Calheta GCI", "Calheta"],
             ["Calheta", "Calheta"],
             ["Flamengos", "Calheta"],
             ["MIGUEL GOMES", "Calheta"],
             ["PIZARRA", "Calheta"],
             ["RIBEIRA PILÃO BRANCO", "Calheta"],
             ["Roteiro IP CALHETA", "Calheta"],
             ["Veneza", "Calheta"],
             ["ADS - Santa Cruz", "Santa Cruz"],
             ["ORGÃOS", "Santa Cruz"],
             ["Roteiro IP SANTA CRUZ", "Santa Cruz"],
             ["SANTA CRUZ GCI", "Santa Cruz"],
             ["SANTA CRUZ RP", "Santa Cruz"],
             ["SANTA CRUZ RURAL", "Santa Cruz"],
             ["SANTA CRUZ SA", "Santa Cruz"],
             ["VILA PEDRA BADEJO", "Santa Cruz"],
             ["IP MOSTEIROS", "Mosteiros"],
             ["MOSTEIROS GC", "Mosteiros"],
             ["Mosteiro-Rural", "Mosteiros"],
             ["Mosteiros", "Mosteiros"],
             ["CLIENTES BT", "São Filipe"],
             ["Clientes IP", "São Filipe"],
             ["CLIENTES MT", "São Filipe"],
             ["SAO FILIPE GC", "São Filipe"],
             ["Barreiro-Rural", "Maio"],
             ["Calheta-Rural", "Maio"],
             ["Figueira da Horta/Seca-Rural", "Maio"],
             ["IP MAIO", "Maio"],
             ["MAIO GC", "Maio"],
             ["Morrinho-Rural", "Maio"],
             ["Morro-Rural", "Maio"],
             ["NORTE RURAL", "Maio"],
             ["Ribeira D.João-Rural", "Maio"],
             ["VILA P.Ingles", "Maio"],
             ["BRAVA GC", "Brava"],
             ["IP BRAVA", "Brava"],
             ["NSM Rural", "Brava"],
             ["SJB Rural", "Brava"],
             ["VN Sintra", "Brava"]
             ]
    uc = pd.DataFrame(dados, columns=['Roteiro', 'Unidade'])
    uc.head()

    # Definir Unidade nos IT's
    unit = pd.merge(itfun, uc, on='Roteiro', how='left')
    unit.head()

    #junção de contador + função + cil
    unit['CIL/Contador/Função'] = unit['CIL'].astype(str) + '-' + unit['Número'].astype(str) + '-' + itfun['Descrição']
    unit['CIL/Contador'] = unit['CIL'].astype(str) + '-' + unit['Número'].astype(str)
    unit.head()

#importar contadores remota
upload_file = st.file_uploader("Importar Contadores Remota", type="xlsx")
if upload_file:
    st.markdown("---")
    contador = carregar_contador()
    contador.head()

    # alterar ordem no contador
    contador['CIL/Contador'] = contador['CIL'].astype(str) + '-' + contador['Nº Contador'].astype(str)
    contador2 = contador.loc[:,
                ['CIL/Contador', 'Nº Contador']
                ]
    # Definir remota
    contador2.loc[contador2['Nº Contador'] >= 0, "Tipo Contador"] = "Leitura Remota"
    contador2.head()

    # noinspection PyUnboundLocalVariable
    unit2 = pd.merge(unit, contador2, on='CIL/Contador', how='left')
    unit.head()

#importar leitura remota
upload_file = st.file_uploader("Importar Leitura Remota", type="xlsx")
if upload_file:
    st.markdown("---")
    remota = carregar_remota()
    remota.head()

    #junção e organização de leitura remota
    remota['CIL/Contador/Função'] = remota['CIL'].astype(str) + '-' + remota['Meter No.'].astype(str) + '-' + \
                                    remota['Descrição']
    remota.head()
    # alterar ordem e apresentar os dados para cruzamento
    remota2 = remota.loc[:,
              ['CIL/Contador/Função', 'Data Time', 'Leitura']]
    remota2.head()

    # cruzar leitura remota e itinerarios
    # noinspection PyUnboundLocalVariable
    geral = pd.merge(unit2, remota2, on='CIL/Contador/Função', how='left')
    geral.head()

    # organizar
    geral2 = geral.loc[:,
             ['Unidade', 'Tipo Contador', 'Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente',
              'Ponto de Medida', 'CIL',
              'Número', 'Marca', 'Função',
              'Anterior', 'Leitura', 'Anomalia']]

    # alterar nome de coluna leitura para atual
    geral3 = geral2.rename(columns={'Leitura': 'Atual'})

    # definir coluna com condições
    geral3['Diferença'] = geral3['Atual'] - geral3['Anterior']

    geral3.loc[geral3['Diferença'] < 0, "Analise Leitura"] = "Volta de Contador"
    geral3.loc[geral3['Diferença'] == 0, "Analise Leitura"] = "Contador Parado"
    geral3.loc[geral3['Diferença'] > 0, "Analise Leitura"] = "Local Com Consumo"
    geral3.head()

    # alterar ordem de apresentação
    geral4 = geral3.loc[:,
             ['Unidade', 'Analise Leitura', 'Tipo Contador', 'Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ',
              ' Rua ', ' Cliente',
              'Ponto de Medida', 'CIL',
              'Número', 'Marca', 'Função',
              'Anterior', 'Atual', 'Anomalia'
              ]]


    st.markdown("---")

    st.subheader("Pré-Visualização de IT's")

    # definir campos de pesquisa
    st.sidebar.header("Definir Itinerário e Roteiro:")
    un = st.sidebar.multiselect(
        "Filtrar Unidade",
        options=geral4['Unidade'].unique(),

    )
    rot = st.sidebar.multiselect(
        "Filtrar Roteiro",
        options=geral4['Roteiro'].unique(),

    )
    it = st.sidebar.multiselect(
        "Filtrar Roteiro",
        options=geral4['Itinerário'].unique(),

    )

    geral_selection = geral4.query(
        "`Unidade` == @un & `Roteiro` == @rot & `Itinerário` == @it"
    )

    # alterar ordem para apresentação e extração
    geral5 = geral_selection.loc[:,
             ['Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente', 'Ponto de Medida', 'CIL',
              'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']
             ]


    # remover coluna de index
    geral5.set_index('Nr. Roteiro', inplace=True)

    # noinspection PyUnboundLocalVariable
    st.dataframe(geral5)

    # converção do ficheiro para o formato csv e baixar o mesmo
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(sep=';').encode('utf-8-sig')


    csv = convert_df(geral5)

    st.download_button(
        label="Download IT",
        data=csv,
        file_name='IT.csv',
        mime='text/csv',
    )

    st.markdown("---")

    st.markdown("---")

    st.subheader("Analise de Leituras Remotas")
    # definir campos de pesquisa
    st.sidebar.header("Analise Leitura:")

    tipo = st.sidebar.multiselect(
        "Filtrar Tipo Contador",
        options=geral4['Tipo Contador'].unique(),

    )
    estado = st.sidebar.multiselect(
        "Filtrar Leitura",
        options=geral4['Analise Leitura'].unique(),

    )
    geral_selection2 = geral4.query(
        "`Tipo Contador` == @tipo & `Analise Leitura` == @estado"
    )

    # alterar ordem para apresentação e extração
    geral6 = geral_selection2.loc[:,
             ['Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente', 'Ponto de Medida', 'CIL',
              'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']
             ]

    # remover coluna de index
    geral6.set_index('Nr. Roteiro', inplace=True)

    st.dataframe(geral6)


    # converção do ficheiro para o formato csv e baixar o mesmo
    @st.cache_data
    def convert_df2(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(sep=';').encode('utf-8-sig')


    csv = convert_df2(geral6)

    st.download_button(
        label="Download Analise",
        data=csv,
        file_name='Analise Leitura.csv',
        mime='text/csv',
    )



