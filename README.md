
# WASTIMIZER - Website para optimizar a gestão de resíduos de uma empresa 
# WASTIMIZER - *Website to optimize a company's waste management*
#### Video Demo:  <URL HERE>
<br>
<br>
<br>

### ÂMBITO
### *SCOPE*
**Português (PT)**: Wastimizer é um website desenvolvido para a gestão eficiente de resíduos em empresas que produzem grandes volumes de resíduos, seja na construção civil ou em qualquer outro setor industrial. O Wastimizer foi desenhado com base na legislação portuguesa e europeia, atendendo também às necessidades de reporte à APA – Agência Portuguesa do Ambiente. <br> ***English (EN)**: Wastimizer is a website designed for efficient waste management in companies that produce large volumes of waste, whether in construction or any other industrial sector. Wastimizer was developed based on Portuguese and European legislation, also addressing the reporting requirements to APA – Portuguese Environment Agency.*
<br>
<br>
<br>

### Descrição de cada template
### *Description of each template*
#### layout.html
**PT**: Este template serve como layout base para a aplicação web "Wastimizer". Ele define a estrutura geral da página, incluindo as configurações de codificação e as referências a estilos e scripts externos. No cabeçalho, estão incluídos metadados, links para o Bootstrap (para estilização responsiva) e a biblioteca SheetJS (para exportação de tabelas para Excel). O título da página é dinâmico, permitindo que diferentes títulos sejam definidos em outros templates através do bloco "{% block title %}{% endblock %}". No corpo da página, existe uma barra de navegação que se adapta consoante a sessão do utilizador. Se o utilizador estiver autenticado, são exibidos links para várias seções da aplicação, como "Estabelecimentos", "LER", "Operações", "Inserir e-GAR's", "Mapa" e "MIRR", além de uma opção para sair. Se o utilizador não estiver autenticado, são apresentados links para registo e login, juntamente com o logotipo da aplicação. Além disso, o layout inclui um sistema para exibir mensagens de feedback (flash messages) ao utilizador, que aparecem em destaque em caso de qualquer notificação. O bloco "{% block main %}{% endblock %}" permite que outros templates insiram conteúdo específico dentro do corpo da página. <br> ***EN**: This template serves as the base layout for the web application "Wastimizer." It defines the overall structure of the page, including encoding settings and references to external styles and scripts. In the header, metadata, links to Bootstrap (for responsive styling), and the SheetJS library (for exporting tables to Excel) are included. The page title is dynamic, allowing different titles to be defined in other templates through the block "{% block title %}{% endblock %}". In the body of the page, there is a navigation bar that adapts based on the user's session. If the user is authenticated, links to various sections of the application, such as "Establishments," "LER," "Operations," "Insert e-GARs," "Map," and "MIRR," are displayed, along with an option to log out. If the user is not authenticated, links for registration and login are presented, along with the application's logo. Additionally, the layout includes a system for displaying feedback messages (flash messages) to the user, which appear prominently in case of any notifications. The block "{% block main %}{% endblock %}" allows other templates to insert specific content within the body of the page.*
<br>

#### register.html
**PT**: O utilizador faz o registo no website. Para o efeito tem que escolher o nome de utilizador, palavra-passe e confirmação da palavra-passe escolhida. Após o sucesso deste registo, o utilizador pode efetuar o login. <br>***EN**: The user registers on the website. To do this, they must choose a username, password, and confirm the chosen password. After successful registration, the user can log in.*
<br>
#### login.html
**PT**: Após realizado o registo no website, o utilizador pode fazer login usando as credencias de acesso: Nome de utilizador e palavra-passe. <br>***EN**: After registering on the website, the user can log in using their access credentials: Username and password.*
<br>
#### establishments.html
**PT**: Este template é utilizado para gerir estabelecimentos relacionados com a Agência Portuguesa do Ambiente (APA). A página é intitulada "Estabelecimentos". O utilizador pode inserir novos estabelecimentos através de um formulário que contém os seguintes campos: Código APA (formatos aceites são "APAXXXXXXXX" ou "GT"), Nome completo do estabelecimento e Nome curto do estabelecimento. Está disponível um botão "Gravar" para submeter o formulário e guardar o novo estabelecimento. Uma tabela exibe todos os estabelecimentos já registados, mostrando as seguintes informações: Código APA, Nome completo e Nome curto. Para cada estabelecimento listado na tabela, o utilizador pode apagar ou editar o registo. O botão "Apagar" exibe um formulário de confirmação com um aviso sobre a irreversibilidade da ação, permitindo que o utilizador confirme ou cancele a eliminação. O botão "Editar" exibe um formulário de edição pré-preenchido com os dados atuais do estabelecimento, permitindo que o utilizador altere o Código APA, Nome completo e Nome curto. As alterações podem ser aplicadas clicando no botão "Aplicar alterações". Existem scripts JavaScript embutidos que gerem a exibição dos formulários de confirmação de eliminação e edição, garantindo uma experiência de uso intuitiva e funcional. <br>***EN**: This template is used to manage establishments related to the Portuguese Environment Agency (APA). The page is titled "Establishments." The user can enter new establishments through a form that contains the following fields: APA Code (accepted formats are "APAXXXXXXXX" or "GT"), Full name of the establishment , and Short name of the establishment. A "Save" button is available to submit the form and save the new establishment. A table displays all registered establishments, showing the following information: APA Code, Full name, and Short name. For each establishment listed in the table, the user can delete or edit the record. The "Delete" button shows a confirmation form with a warning about the irreversibility of the action, allowing the user to confirm or cancel the deletion. The "Edit" button displays a pre-filled edit form with the current data of the establishment, allowing the user to change the APA Code, Full name, and Short name. Changes can be applied by clicking the “Aplicar Alterações” ("Apply Changes") button. There are embedded JavaScript scripts that manage the display of confirmation forms for deletion and editing, ensuring an intuitive and functional user experience.*
<br>

#### codler_description.html
**PT**: Este template é utilizado para gerir códigos LER (Lista Europeia de Resíduos) e suas descrições. A página é intitulada "LER". O utilizador pode inserir novos códigos LER através de um formulário que contém os seguintes campos: Código LER (no formato "XX XX XX" ou "XXXXXX") e Descrição LER. Está disponível um botão "Gravar" para submeter o formulário e guardar o novo código LER. Uma tabela exibe todos os códigos LER já registados, mostrando as seguintes informações: Código LER e Descrição. Para cada código listado na tabela, o utilizador pode apagar ou editar o registo. O botão "Apagar" exibe um formulário de confirmação com um aviso sobre a irreversibilidade da ação, permitindo que o utilizador confirme ou cancele a eliminação. O botão "Editar" exibe um formulário de edição pré-preenchido com os dados atuais do código LER, permitindo que o utilizador altere o Código LER e a Descrição. As alterações podem ser 
aplicadas clicando no botão "Aplicar alterações". Existem scripts JavaScript embutidos que gerem a exibição dos formulários de confirmação de eliminação e edição, garantindo uma experiência de uso intuitiva e funcional. <br>***EN**: This template is used to manage LER codes (European Waste List) and their descriptions. The page is titled "LER." The user can enter new LER codes through a form that contains the following fields: LER Code (in the format "XX XX XX" or "XXXXXX") and LER Description. A “Guardar”("Save") button is available to submit the form and save the new LER code. A table displays all registered LER codes, showing the following information: LER Code and Description. For each code listed in the table, the user can delete or edit the record. The “Apagar”("Delete") button shows a confirmation form with a warning about the irreversibility of the action, allowing the user to confirm or cancel the deletion. The "Edit" button displays a pre-filled edit form with the current data of the LER code, allowing the user to change the LER Code and Description. Changes can be applied by clicking the “Aplicar Alterações”("Apply Changes") button. There are embedded JavaScript scripts that manage the display of confirmation forms for deletion and editing, ensuring an intuitive and functional user experience.*
<br>

#### operation_description.html
**PT**: Este template é utilizado para gerir operações de valorização e eliminação, com foco no destino final. A página é intitulada "Operations". O utilizador pode inserir novas operações através de um formulário que contém os seguintes campos: Operação de valorização/eliminação (destino final) e Descrição da operação. Está disponível um botão "Gravar" para submeter o formulário e guardar a nova operação. Uma tabela exibe todas as operações já registadas, mostrando as seguintes informações: Operação e Descrição. Para cada operação listada na tabela, o utilizador pode apagar ou editar o registo. O botão "Apagar" exibe um formulário de confirmação com um aviso sobre a irreversibilidade da ação, permitindo que o utilizador confirme ou cancele a eliminação. O botão "Editar" exibe um formulário de edição pré-preenchido com os dados atuais da operação, permitindo que o utilizador altere a Operação e a Descrição. As alterações podem ser aplicadas clicando no botão "Aplicar alterações". Existem scripts JavaScript embutidos que gerem a exibição dos formulários de confirmação de eliminação e edição, garantindo uma experiência de uso intuitiva e funcional. <br> ***EN**: This template is used to manage recovery and disposal operations, focusing on the final destination. The page is titled "Operations." The user can enter new operations through a form that contains the following fields: Valorization/Elimination Operation (final destination) and Description of the operation. A "Guardar"("Save") button is available to submit the form and save the new operation. A table displays all registered operations, showing the following information: Operation and Description. For each operation listed in the table, the user can delete or edit the record. The "Delete" button shows a confirmation form with a warning about the irreversibility of the action, allowing the user to confirm or cancel the deletion. The "Edit" button displays a pre-filled edit form with the current data of the operation, allowing the user to change the Operation and Description. Changes can be applied by clicking the "Aplicar Alterações"("Apply Changes") button. There are embedded JavaScript scripts that manage the display of confirmation forms for deletion and editing, ensuring an intuitive and functional user experience.*
<br>

#### insert.html
**PT**: Este template é utilizado para inserir e-GAR (Guia de Acompanhamento de Resíduos) na aplicação. A página é intitulada "Insert". O utilizador é apresentado com um formulário que permite introduzir várias informações relevantes, incluindo a data do e-GAR, o número do e-GAR, e a obra associada. O formulário contém campos para selecionar o transportador, incluindo nome, NIF e matrícula, bem como a APA do transportador. Além disso, o utilizador deve preencher detalhes sobre a operação de valorização/eliminação, como o código LER, a tonelagem e o destino final dos resíduos. O formulário também requer informações sobre o destinatário, incluindo nome, APA e NIF, assim como o produtor do resíduo, que pode ser selecionado de uma lista ou indicado como "Outro". O botão "Submeter" permite que o utilizador envie os dados inseridos para processamento. O layout é responsivo e utiliza classes do Bootstrap para garantir uma boa apresentação em diferentes dispositivos. <br>***EN**: This template is used to insert e-GAR (Waste Tracking Guide) into the application. The page is titled "Insert." The user is presented with a form that allows them to enter various relevant information, including the date of the e-GAR, the e-GAR number, and the associated project. The form contains fields to select the transporter, including name, NIF (Tax Identification Number), and license plate, as well as the APA of the transporter. Additionally, the user must provide details about the valorization/elimination operation, such as the LER code, tonnage, and the final destination of the waste. The form also requires information about the recipient, including name, APA, and NIF, as well as the waste producer, which can be selected from a list or indicated as "Outro"("Other"). The "Submeter"("Submit") button allows the user to send the entered data for processing. The layout is responsive and uses Bootstrap classes to ensure good presentation across different devices.*
<br>

#### history.html
**PT**: Este template é utilizado para apresentar o "Mapa de Resíduos" na aplicação. A página, intitulada "History", permite ao utilizador filtrar dados de resíduos por empreitada e ano, além de oferecer uma opção para incluir armazenamento preliminar e recolhas na sede da empresa. O utilizador pode escolher entre várias opções disponíveis em listas suspensas. No topo da página, há um botão para exportar os dados apresentados na tabela para um arquivo Excel. A tabela exibe informações detalhadas sobre os resíduos, incluindo a data, número de e-GAR, obra, transportador, código LER, quantidade, destino final, e informações sobre o destinatário e produtor. Cada linha da tabela inclui botões para editar ou apagar entradas. Ao clicar em "Apagar", o utilizador confirma a exclusão, enquanto a opção "Editar" permite modificar os dados existentes. A tabela é responsiva e utiliza classes do Bootstrap para garantir uma apresentação adequada em diferentes dispositivos. <br>***EN**: This template is used to present the "Waste Map" in the application. The page, titled "History," allows the user to filter waste data by project and year, as well as offering an option to include preliminary storage and pickups at the company's headquarters. The user can choose from various options available in dropdown lists. At the top of the page, there is a button to export the data presented in the table to an Excel file. The table displays detailed information about the waste, including the date, e-GAR number, project, transporter, LER code, quantity, final destination, and information about the recipient and producer. Each row of the table includes buttons to edit or delete entries. Clicking "Apagar"("Delete") prompts the user to confirm the deletion, while the "Editar"("Edit") option allows modification of existing data. The table is responsive and uses Bootstrap classes to ensure proper presentation across different devices.*
<br>

#### mirr.html
**PT**: Este template é utilizado para o "Mapa Integrado de Registo de Resíduos" (MIRR). O MIRR é uma formalidade que deve ser apresentada todos os anos à APA (Agência Portuguesa do Ambiente), no âmbito da Campanha Anual de Reporte. A estrutura do MIRR difere da do mapa de resíduos (history), pois agrupa os dados por código LER, código APA do destinatário, designação do destinatário (OGR - Operador de Gestão de Resíduos), transportador (empresa responsável pelo transporte dos resíduos da obra para o destinatário/OGR) e operação de valorização/eliminação. Além disso, são apresentados os totais de resíduos (tonelagem) consoante estes agrupamentos. A página permite ao utilizador filtrar os dados do MIRR por estabelecimento e ano. Os utilizadores podem escolher entre opções de estabelecimentos e selecionar o ano desejado para gerar o relatório. No topo da página, existe um botão para exportar os dados da tabela para um arquivo Excel. A tabela apresenta informações detalhadas, incluindo o código LER, quantidade de resíduos por tipo, destinatário, NIF do destinatário, APA do destinatário, operação realizada, quantidade por empresa e detalhes sobre o transportador. Os dados são apresentados de forma clara e organizada, utilizando classes do Bootstrap para garantir uma boa apresentação visual. A funcionalidade de exportação para Excel é implementada com a biblioteca SheetJS, facilitando o download dos dados para análise posterior. <br> ***EN**: This template is used for something similiar to "Integrated Waste Registration Map" (MIRR). The MIRR is a formal requirement that must be submitted annually to the APA (Portuguese Environment Agency) as part of the Annual Reporting Campaign. The structure of the MIRR differs from that of the waste map (history) as it groups data by LER code, APA code of the recipient, designation of the recipient (OGR - Waste Management Operator), transporter (the company responsible for transporting the waste from the project to the recipient/OGR), and valorization/elimination operation. Additionally, total waste (tonnage) is presented according to these groupings. The page allows the user to filter MIRR data by establishment and year. Users can choose from options for establishments and select the desired year to generate the report. At the top of the page, there is a button to export the table data to an Excel file. The table presents detailed information, including LER code, quantity of waste by type, recipient, NIF of the recipient, APA of the recipient, operation performed, quantity by company, and details about the transporter. The data is presented clearly and organized, using Bootstrap classes to ensure good visual presentation. The export to Excel functionality is implemented with the SheetJS library, facilitating the download of data for later analysis.*
<br>

#### apology.html
**PT**: Este template é projetado para exibir uma mensagem de desculpa (mensagem de erro) ao utilizador. O título da página é definido como "Apology". No bloco principal, apresenta-se uma mensagem personalizada, armazenada na variável "{{ message }}", que é exibida durante o processo de registo e/ou login, esclarecendo a situação ao utilizador. Adicionalmente, um segundo elemento exibe o valor da variável "{{ code }}", que corresponde a um códido de erro (Status). O layout é estilizado com classes CSS, garantindo que a apresentação visual da mensagem seja clara e informativa. <br> ***EN**: This template is designed to display an apology message to the user. The page title is set as "Apology." In the main block, a personalized message stored in the variable "{{ message }}" is presented, displayed during the registration and/or login process, clarifying the situation to the user. Additionally, a second element shows the value of the variable "{{ code }}", which corresponds to an error code (Status). The layout is styled with CSS classes, ensuring that the visual presentation of the message is clear and informative.*
<br>
<br>
<br>

### Ficheiros Python: app.py e helpers.py
### *Python Files: app.py and helpers.py*
#### app.py
**PT**: O ficheiro app.py serve como o núcleo da aplicação web Wastimizer, que visa otimizar a gestão de resíduos em empresas. Desenvolvida em Flask, esta aplicação permite o gerenciamento eficaz de informações relacionadas com resíduos, assegurando a conformidade com a legislação portuguesa e europeia. **Registo e Login**: As rotas '/register' e '/login' permitem que os utilizadores criem contas e realizem autenticação. O processo de registo requer a escolha de um nome de utilizador e palavra-passe, enquanto o login valida essas credenciais, iniciando a sessão e permitindo acesso a funcionalidades restritas; **Gestão de Estabelecimentos**: Na rota '/establishments', os utilizadores podem adicionar, editar ou eliminar estabelecimentos vinculados à Agência Portuguesa do Ambiente (APA). A interface é intuitiva, apresentando um formulário para inserção de novos dados e uma tabela que lista todos os estabelecimentos registados, com opções para ações de edição e exclusão; **Códigos LER**: A rota '/codler_description' permite a gestão dos códigos da Lista Europeia de Resíduos. Os utilizadores têm a possibilidade de inserir novos códigos através de um formulário, e podem também visualizar, editar ou remover códigos existentes, com um enfoque na clareza e eficiência dos dados; **Operações de Valorização e Eliminação**: A gestão de operações de valorização e eliminação é realizada na rota '/operations'. Aqui, os utilizadores inserem informações sobre operações específicas, que são apresentadas de forma organizada em tabelas, incluindo funcionalidades para edição e eliminação, garantindo um manuseio eficaz dos dados; **Inserção de e-GAR**: A rota '/insert' é dedicada à inserção de e-GAR (Guias de Acompanhamento de Resíduos). Através de um formulário detalhado, os utilizadores podem introduzir todas as informações relevantes, como a data da e-GAR, número, transportador e dados do destinatário. Esta funcionalidade é fundamental para o cumprimento das obrigações legais em matéria de gestão de resíduos; **Mapa de Resíduos e MIRR**: As rotas '/history' e '/mirr' são utilizadas para apresentar, respetivamente, o Mapa de Resíduos e o Mapa Integrado de Registo de Resíduos (MIRR). Estas páginas oferecem opções de filtragem por ano e estabelecimento, e incluem a capacidade de exportar os dados apresentados para arquivos Excel, facilitando análises posteriores. As diferenças ente Mapa de Resíduos e MIRR estão explicadas na secção anterior "Descrição de cada template". <br>***EN**: The file app.py serves as the core of the Wastimizer web application, aimed at optimizing waste management in companies. Developed in Flask, this application allows for effective management of waste-related information, ensuring compliance with Portuguese and European legislation. **Registration and Login**: The '/register' and '/login' routes enable users to create accounts and authenticate. The registration process requires selecting a username and password, while login validates these credentials, initiating the session and granting access to restricted features; **Establishment Management**: On the '/establishments' route, users can add, edit, or delete establishments linked to the Portuguese Environment Agency (APA). The interface is intuitive, presenting a form for inputting new data and a table listing all registered establishments, with options for editing and deleting actions; **LER Codes**: The '/codler_description' route allows for the management of European Waste List codes. Users have the option to enter new codes via a form, and can also view, edit, or remove existing codes, focusing on clarity and efficiency of data; **Valorization and Elimination Operations**: The management of recovery and disposal operations is conducted on the '/operations' route. Here, users input information about specific operations, which are presented in an organized manner in tables, including functionalities for editing and deleting, ensuring effective data handling; **Inserting e-GAR**: The '/insert' route is dedicated to inserting e-GAR (Waste Tracking Guides). Through a detailed form, users can input all relevant information, such as the e-GAR date, number, transporter, and recipient data. This functionality is crucial for meeting legal obligations regarding waste management; **Waste Map and MIRR**: The '/history' and '/mirr' routes are used to present the Waste Map and the Integrated Waste Registration Map (MIRR), respectively. These pages offer filtering options by year and establishment, and include the ability to export the displayed data to Excel files, facilitating further analysis. The differences between the Waste Map and MIRR are explained in the previous section *"Description of each template"*.*
<br>

#### helpers.py
**PT**: **Funções e Decoradores**: **Função "apology"**: Renderiza uma mensagem de desculpa para o utilizador. A função inclui uma subfunção escape que escapa caracteres especiais conforme especificado, permitindo uma apresentação adequada na interface; **Função "login_required(f)"**: Decorador que protege rotas, exigindo que o utilizador esteja autenticado. Se o utilizador não estiver logado, será redirecionado para a página de login; **Formatação de Dados**: **format_codLER(value)**: Formata códigos "LER" para um dos dois formatos permitidos: "XX XX XX" ou "XXXXXX". Valida o formato do código introduzido e, se válido, realiza a formatação apropriada; **format_codLER_excel(value)**: Prepara o código "LER" para exportação em Excel, adicionando o prefixo "LER " ao código fornecido, assegurando que esteja no formato correto para tabelas; **format_ton(value)**: Formata valores em toneladas com precisão de três casas decimais, utilizando separadores de milhar para facilitar a leitura. <br>***EN**: **Functions and Decorators**: **Function "apology"**: Renders an apology message to the user. The function includes a subfunction escape that escapes special characters as specified, allowing for proper presentation in the interface; **Function "login_required(f)"**: A decorator that protects routes, requiring the user to be authenticated. If the user is not logged in, they will be redirected to the login page; **Data Formatting**: **format_codLER(value)**: Formats "LER" codes to one of the two allowed formats: "XX XX XX" or "XXXXXX". It validates the format of the entered code and, if valid, performs the appropriate formatting; **format_codLER_excel(value)**: Prepares the "LER" code for export to Excel by adding the prefix "LER " to the provided code, ensuring it is in the correct format for tables; **format_ton(value)**: Formats ton values to three decimal places, using thousand separators for improved readability.*
<br>
<br>
<br>

### Ficheiros Static
### *Static Files*
#### style.css
**PT**: O ficheiro style.css define uma parte do estilo visual da aplicação web Wastimizer, melhorando a interface do utilizador com estilos personalizados para a navegação, botões e tabelas. As regras de estilo da barra de navegação personalizam a aparência dos elementos, incluindo o tamanho e a cor da fonte, com efeitos de hover que alteram a cor do texto para melhorar a interatividade. Os botões de "logout", "registo" e "login" também possuem estilos específicos, incluindo tamanhos e cores de fonte, além de estados ativos que criam um efeito de clique com alterações na cor de fundo e sombreamento. O ficheiro define ainda cores de fundo para várias secções, na tentativa de garantir uma estética coesa em toda a aplicação. No que diz respeito à formatação de tabelas, estabelece estilos para tabelas de entrada e saída, incluindo famílias de fontes, espaçamento e efeitos de hover para melhorar a legibilidade e usabilidade, com cores de linha alternadas para uma melhor distinção visual. Em suma, este ficheiro CSS contribui para uma interface intuitiva, promovendo a facilidade de navegação e gestão de dados na aplicação. <br> ***EN**: The style.css file defines part of the visual style of the Wastimizer web application, enhancing the user interface with custom styles for navigation, buttons, and tables. The navigation bar style rules customize the appearance of elements, including font size and color, with hover effects that change the text color to improve interactivity. The "logout," "register," and "login" buttons also have specific styles, including font sizes and colors, as well as active states that create a click effect with changes in background color and shadowing. The file also defines background colors for various sections to ensure a cohesive aesthetic throughout the application. Regarding table formatting, it establishes styles for input and output tables, including font families, padding, and hover effects to enhance readability and usability, with alternating row colors for better visual distinction. In summary, this CSS file contributes to an intuitive interface, promoting ease of navigation and data management within the application.*
<br>

#### wastimizerLogo.png
**PT**: Logo "Wastimizer" - ver secção de Agradecimentos
<br>
***EN**: Logo "Wastimizer" - See Acknowledgements section*
<br>
<br>
<br>

### Melhorias a realizar
### *Improvements to be made*
**PT**:
+ Recuperação de palavra-passe
+ Garantir maior força na palavra-passe que é escolhida pelo utilizador
+ Adicionar botão para eliminar data específica (ex: Eliminar toda a informação relativa a um ano específico ou estabelecimento/obra)
<br>

**EN**:
+ *Password recovery*
+ *Ensure greater strength in the password chosen by the user*
+ *Add a button to eliminate specific data (e.g., eliminate all the information from a specific year or establishment/contractor).*
<br>
<br>
<br>

### Agradecimentos
### *Acknowledgements*
**PT**
Logo "Wastimizer" desenhado por [Elsa Ferreira]
<br>
**EN**
*Logo "Wastimizer" designed by [Elsa Ferreira]*
<br>
<br>
<br>


### Autor do Projecto
### Project Author
*Vasco Nogueira da Rocha - <https://github.com/VascoNog/>*


