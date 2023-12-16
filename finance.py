from flet import *
from datetime import datetime
import sqlite3
from math import pi
from time import sleep
import threading
import pyperclip
import locale
from dateutil.relativedelta import relativedelta
import locale
import pandas as pd
import os

# Classe banco de dados Contas
class Database:

    def ConnectToDatabase():
        try:
            db = sqlite3.connect("finanças.db")

            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE if not exists tasks (
                    id INTEGER PRIMARY KEY,
                    Task VARCHAR(255) NOT NULL,
                    Gasto VARCHAR(255),
                    Pago INTEGER DEFAULT 0 CHECK (Pago IN (0, 1)),
                    Mes VARCHAR(255) NOT NULL,
                    Data_vencimento VARCHAR(255),
                    Data_pagamento VARCHAR(255),
                    Data_entrada VARCHAR(255)
                    
                    
                )
            ''')

            return db

        except Exception as e:
            print(e)


    def ReadDatabase(db):

        cursor = db.cursor()

        cursor.execute("SELECT Task, Gasto, Pago, Mes, Data_vencimento, Data_pagamento, Data_entrada FROM tasks")
        results = cursor.fetchall()
        return results

    def InsertDatabase(db, values):
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (Task, Gasto, Mes, Data_vencimento, Data_entrada) VALUES (?,?,?,?,?)", values)
        db.commit()

    def DeleteDatabase(db, Task, vencimento):

        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE Task=? AND Data_vencimento=?", (Task, vencimento))
        db.commit()



    def UpdateDatabase(db, new_name, new_price, data_vencimento, old_name, old_data):
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET Task=?, Gasto=?, Data_vencimento=? WHERE Task=? AND Data_vencimento=?", (new_name, new_price, data_vencimento, old_name, old_data))
        db.commit()

# Classe para adicionar novas contas
class FormContainer(UserControl):
    def __init__(self):
        

        super().__init__()
    

    def build(self):
        return Container(
            width=400,
            height=0,
            bgcolor="#1F2128",
            opacity=0,
            border_radius=30,
            margin=margin.only(left=-18, right=-18),
            animate=animation.Animation(400, 'decelerate'),
            animate_opacity=800,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[

                    TextField(
                        height=30,
                        width=250,
                        filled=True,
                        border_radius=20,
                        color="white",
                        border_color="transparent",
                        hint_text="Nome da Nova Conta:",
                        text_align="center",
                        hint_style=TextStyle(size=12, color=colors.BLUE_200),
                        bgcolor="#17181d",
                    
     
                    ),

                    TextField(
                        height=30,
                        width=250,
                        filled=True,
                        border_radius=20,
                        color="white",
                        border_color="transparent",
                        hint_text="Valor da Conta:",
                        text_align="center",
                        hint_style=TextStyle(size=12, color=colors.BLUE_200),
                        bgcolor="#17181d",
                        
                        
                    ),

                    ElevatedButton(
                        "Vencimento",
                        icon=icons.CALENDAR_MONTH,
                        on_click=None,
                        bgcolor="#12121a"
                    ),


                    Row(
                        alignment="center",
                        controls=[
                        Checkbox(
                            label="Clonar Conta", 
                            value=False,
                            )
                    ]),
                    Divider(height=5, color="transparent"),
                    ElevatedButton(
                        text="Adicionar",
                        width=150,
                        icon=icons.DONE,
                        on_click=None,
                        bgcolor="#12121a",
                    ),
                    
                ],
            )
        )

# Classe para gerar as contas quando o usuario adicionar
class Createtask(UserControl):
    def __init__(self, task:str, date:str, color:str, func1, func2, func3):

        self.task = task
        self.date = date
        self.color = color
        self.func1 = func1
        self.func2 = func2
        self.func3 = func3
        super().__init__()

    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click= lambda e: func(self.GetContainerInstance())
        )


    def GetContainerInstance(self):
        return self



    def ShowIcons(self, e):

        name = e.control.content.controls[0].controls[0].value
        
        if " - PAGO" in name:
            e.control.content.controls[1].controls[2].opacity = 1
            e.control.content.controls[1].controls[0].opacity = 0
            e.control.content.controls[1].controls[1].opacity = 0
            e.control.content.update()

        else:
            
            if e.data == "true":
                
                (
                    e.control.content.controls[1].controls[0].opacity,
                    e.control.content.controls[1].controls[1].opacity,
                    e.control.content.controls[1].controls[2].opacity,
                ) = (1,1,1)
                e.control.content.update()
            else:
                (
                    e.control.content.controls[1].controls[0].opacity,
                    e.control.content.controls[1].controls[1].opacity,
                    e.control.content.controls[1].controls[2].opacity,
                ) = (0,0,0)
                e.control.content.update()


    def build(self):
        return Container(
            width=350,
            height=70,
            border=border.all(0.85, "white54"),
            border_radius=20,
            on_hover=lambda e:self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=14, color=self.color),
                            Text(value=self.date, size=11, color='white54'),
                        ],
                    ),

                    Row(
                        spacing=10,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(icons.DELETE_ROUNDED, "red500", self.func1,),
                            self.TaskDeleteEdit(icons.EDIT_ROUNDED, "white70", self.func2),
                            self.TaskDeleteEdit(icons.DONE_ALL_ROUNDED, "green",self.func3),
                        ]
                    )



                ],
            ),
        )


class AnimatedBox(UserControl):

    def __init__(self, border_color, bg_color, rotate_angle):

        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle

        super().__init__()



    def build(self):

        return  Container(
            width=78,
            height=78,
            border=border.all(2.5, self.border_color),
            bgcolor=self.bg_color,
            border_radius=2,
            rotate=transform.Rotate(self.rotate_angle, alignment.center),
            animate_rotation=animation.Animation(700, "easeInOut"),
        )

# Classe Database para cartões
class Database_card:



    def ConnetToDatabase_card():
        db = sqlite3.connect("card_data.db")
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE if not exists cards (
                CardName VARCHAR(255) NOT NULL,
                CardNumber VARCHAR(255) NOT NULL,
                CVCNumber VARCHAR(255),
                DataValid VARCHAR(255)
            )
        ''')
        return db




    def ReadDatabase(db):

        cursor = db.cursor()

        cursor.execute("SELECT CardName, CardNumber, CVCNumber, DataValid FROM cards")
        results = cursor.fetchall() 
        return results


    def InsertDatabase(db, values):
        cursor = db.cursor()
        cursor.execute("INSERT INTO cards (CardName, CardNumber, CVCNumber, DataValid) VALUES (?,?,?,?)", values)
        db.commit()


    def DeleteDatabase(db, CardNumber, CVCNumber):

        cursor = db.cursor()
        cursor.execute("DELETE FROM cards WHERE CardNumber=? AND CVCNumber=?", (CardNumber, CVCNumber))
        db.commit()

# Classe para abrir o form Input Card
class FormCard(UserControl):
    def __init__(self):
            

            super().__init__()
        


    def build(self):
        
        return Container(
            width=400,
            height=0,
            bgcolor="#1F2128",
            opacity=0,
            border_radius=20,
            animate=animation.Animation(400, 'decelerate'),
            animate_opacity=800,
            
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                
                controls=[

                    Divider(height=20, color="transparent"),
                    
                    Text("Insira os Dados do Novo Cartão", color="white", size=18, weight="bold"),

                    Divider(height=10, color="transparent"),

                    Dropdown(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Instituição Ficanceira",
                        hint_style=TextStyle(size=15, color="white"),
                        bgcolor=colors.BLACK38,
                        options=[
                            dropdown.Option("Nubank"),
                            dropdown.Option("Santander"),
                            dropdown.Option("Itaú"),
                            dropdown.Option("Caixa"),
                            dropdown.Option("Bradesco"),

                        ]
                    
    
                    ),

                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Numero do Cartão:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                        
                        
                    ),
                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="CVC do Cartão:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                        
                        
                    ),
                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Data de Validade:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                    ),

                    ElevatedButton(
                        content=Text("Adicionar", color="white"),
                            width=130, 
                            height=40,
                            on_click=None,
                            style=ButtonStyle(
                                bgcolor={"": colors.BLACK38},
                                shape={"": RoundedRectangleBorder(radius=20)},

                            ),
                    
                    ),

                    
                ],
            )
        )

# Classe para adicionar novos cartões
class AddCard(UserControl):
    def __init__(self, bank_name: str, card_number:str, card_cvc:str, data_valid: str):

        self.card_number = card_number
        self.card_cvc = card_cvc
        self.bank_name = bank_name
        self.data_valid = data_valid

        super().__init__()

    
    

    def GetValue(self, e):
        valor =  e.control.data

        pyperclip.copy(valor)
        self.snack.open = True
        self.update()


    def build(self):

        

        self.img = Image()

        if self.card_number[0] == "4":
            self.img = Image(
                src="https://img.icons8.com/external-tal-revivo-bold-tal-revivo/384/000000/external-visa-an-american-multinational-financial-services-corporation-logo-bold-tal-revivo.png",
                width=80,
                height=80,
                fit="contain",
            )
        elif self.card_number[0] == "5":
            self.img = Image(
                src="https://img.icons8.com/color/1200/000000/mastercard-logo.png",
                width=80,
                height=80
            )
        else:
            self.img = Image(
                src="https://www.vectorlogo.zone/logos/cartaoelocombr/cartaoelocombr-ar21.svg",
                width=80,
                height=60
            )



        if self.bank_name == "Nubank":
            
            ColorList = {
                "start": ["#9100b3"],
                "end" : ["#3a0147"],
            }
        
        if self.bank_name == "Santander":

            ColorList = {
                "start": ["#eb3434"],
                "end" : ["#330101"],
            }


        if self.bank_name == "Itaú":

            ColorList = {
                "start": ["#e87602"],
                "end" : ["#c26602"],
            }

        if self.bank_name == "Caixa":

            ColorList = {
                "start": ["#003a9e"],
                "end" : ["#3a0147"],
            }

        if self.bank_name == "Bradesco":

            ColorList = {
                "start": ["#eb3434"],
                "end" : ["#003a9e"],
            }


        self.snack = SnackBar(Text(f"Numero do Cartão {self.bank_name} Copiado!"))
        
        return Container(
            border_radius=border_radius.all(20),
            width=300,
            height=200,
            padding=padding.all(10),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=[
                    ColorList["start"][0],
                    ColorList["end"][0],
                ],
            ),
            
            content=Column(
                spacing=-5,
                controls=[
                    self.snack,
                    Container(
                        content=(
                            Text(
                                self.bank_name,
                                size=28,
                                weight="w700"
                            )
                        ),
                        alignment=alignment.top_left,
                    ),
                    Container(
                        padding=padding.only(top=10,bottom=10)

                    ),

                    Row(
                        alignment="spaceBetween",
                        controls=[
                            Column(
                                spacing=1,
                                controls=[
                                    Container(
                                        alignment=alignment.top_right,
                                        content=Text(
                                            f"Data de Validade: {self.data_valid}",
                                            color="gray",
                                            size=10,
                                            weight="w700",
                                        )
                                    ),
                                    Container(
                                        padding=padding.only(top=10,bottom=5)

                                    ),
                                    Container(
                                        alignment=alignment.bottom_left,
                                        content=Text(
                                            "Numero do Cartão",
                                            color="gray",
                                            size=9,
                                            weight="w500",
                                        )
                                    ),
                                    Container(
                                        alignment=alignment.top_left,
                                        content=Text(
                                            f"**** **** **** {self.card_number[-4:]}",
                                            color="e2e8f0",
                                            size=15,
                                            weight="w700",
                                        ),
                                        data=self.card_number,
                                        on_click=lambda e: self.GetValue(e)
                                    ),
                                    Container(
                                        bgcolor="pink",
                                        padding=padding.only(bottom=5)
                                    ),
                                    Container(
                                        alignment=alignment.bottom_left,
                                        content=Text(
                                            "CVV",
                                            color="gray",
                                            size=10,
                                            weight="w500"
                                        )
                                    ),
                                    Container(
                                        alignment=alignment.top_left,
                                        content=Text(
                                            f"**{self.card_cvc[-1:]}",
                                            color="#e2e8f0",
                                            size=13,
                                            weight="w700",
                                        ),
                                        data=self.card_cvc,
                                        on_click=lambda e: self.GetValue(e)
                                    ),
                                ]
                            ),
                            Column(
                                horizontal_alignment="end",
                                controls=[self.img],
                            ),


                        ]
                    ),
                ],
            ),
        )



def main(page: Page):
    page.window_width = 435
    page.window_height = 830
    page.theme_mode = "dark"
    page.bgcolor = "#1F2128"
    page.window_resizable = False
    page.window_maximizable = False



    #INICIO DAS FUNÇÕES E WIDGET DA 1 PAGINA
    def calculate_value():
        value_dropdown = dropdown_mês.value

        db = Database.ConnectToDatabase()

        cursor = db.cursor()

        if value_dropdown is not None and value_dropdown != "Todos Meses":
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 0 AND Mes = ?", (value_dropdown,))
        else:
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 0")


        valor = cursor.fetchone()[0]  

        if not valor:
            valor = 0

        valor_não_pago = Text(f"Não Pago R$ {valor:.2f}", size=13, color="red")


        page.update()

        return valor_não_pago

    def calculate_value_paied():

        value_dropdown = dropdown_mês.value

        db = Database.ConnectToDatabase()

        cursor = db.cursor()

        if value_dropdown is not None and value_dropdown != "Todos Meses":
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 1 AND Mes = ?", (value_dropdown,))

        else:
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 1")


        valor = cursor.fetchone()[0]  

        if not valor:
            valor = 0

        valor_pago = Text(f"Pago R$ {valor:.2f}", size=13, color="green")


        page.update()

        return valor_pago

    def CreateToDoTask(e):
        form_add.content.controls[0].value = None
        form_add.content.controls[1].value = None
        form_add.content.controls[5].text = "Adicionar"
        form_add.content.controls[3].controls[0].disabled = False
        form_add.content.controls[3].controls[0].value = False
        form_add.content.controls[5].on_click = lambda e: AddTaskToScreen(e)
        form_add.content.controls[2].on_click = lambda _: date_picker.pick_date()
        date_picker.value = None
        if form_add.height != 290:
            form_add.height, form_add.opacity = 290, 1
        else:
            form_add.height, form_add.opacity = 0, 0

        form_add.update()

    def DeleteFunction(e):
        
        data_vencimento_completa = e.controls[0].content.controls[0].controls[1].value
        split = data_vencimento_completa.split(": ")
        data_vencimento_split = split[1].strip()
        print(data_vencimento_split)

            
        valor = e.controls[0].content.controls[0].controls[0].value
        name = valor.split(' R$ ')[0]
        
        db = Database.ConnectToDatabase()

        Database.DeleteDatabase(db, name, data_vencimento_split)
        
        db.close()


        firt_page.controls.remove(e)
        firt_page.controls[0].update()


        firt_page.controls[1].controls[0] = calculate_value_paied()

        firt_page.controls[2].controls[0] = calculate_value()

        firt_page.update()

    def UpdateFunction(e):

        form_add.content.controls[2].on_click = lambda _: date_picker.pick_date()
        form_add.content.controls[3].controls[0].disabled = True
        name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]
        price = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[1]


        if " - PAGO" in price:
            price = price.replace(" - PAGO", "")


        (
            form_add.content.controls[0].value,
            form_add.content.controls[1].value,
            form_add.content.controls[5].text,
            form_add.content.controls[5].on_click
        ) = (
            name, price, "Atualizar", lambda _: FinalizeUpdate(e))
        
        if form_add.height == 290 and form_add.opacity == 1:
            form_add.height, form_add.opacity = 0, 0
            form_add.update()
        else:
            form_add.height, form_add.opacity = 290, 1
            form_add.update()

    def FinalizeUpdate(e):
        data_vencimento_completa = e.controls[0].content.controls[0].controls[1].value
        split = data_vencimento_completa.split(": ")
        data_vencimento_old = split[1].strip()

        if form_add.content.controls[0].value and form_add.content.controls[1].value:
            new_name = form_add.content.controls[0].value
            new_price = form_add.content.controls[1].value
            old_name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]
            if date_picker.value:
                data_vencimento = date_picker.value
                new_data_vencimento = data_vencimento.strftime('%d/%m/%Y')
            else:
                new_data_vencimento = data_vencimento_old

            db = Database.ConnectToDatabase()
            Database.UpdateDatabase(db, new_name, new_price, new_data_vencimento, old_name, data_vencimento_old
            )

            
            e.controls[0].content.controls[0].controls[0].value = f"{new_name} R$ {new_price}"
            e.controls[0].content.controls[0].controls[1].value = f"Vencimento: {new_data_vencimento}"
            e.controls[0].content.update()


            firt_page.controls[1].controls[0] = calculate_value_paied()
            firt_page.controls[2].controls[0] = calculate_value()
            firt_page.update()
            
            CreateToDoTask(e)

    def FinalFuncition(e):
        valor = e.controls[0].content.controls[0].controls[0].value
        name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]
        valor_pago = f"{valor} - PAGO"

        data_vencimento_completa = e.controls[0].content.controls[0].controls[1].value
        split = data_vencimento_completa.split(": ")
        data_vencimento_split = split[1].strip()

        data_atual = datetime.now()

        data_pagamento = data_atual.strftime("%d/%m/%Y")
        if " - PAGO" in valor:
            # Remove " - PAGO" se estiver presente no valor
            e.controls[0].content.controls[0].controls[0].value = valor.replace(" - PAGO", "")
            e.controls[0].content.controls[0].controls[0].color = "white"


            db = Database.ConnectToDatabase()

            cursor = db.cursor()
            cursor.execute("UPDATE tasks SET Pago=?, Data_pagamento=? WHERE Task=? AND Data_vencimento=?", (0, None, name, data_vencimento_split))
            db.commit()

            cursor.close()
        else:
            # Adiciona " - PAGO" se não estiver presente no valor
            e.controls[0].content.controls[0].controls[0].value = valor_pago
            e.controls[0].content.controls[0].controls[0].color = "green"
            db = Database.ConnectToDatabase()

            cursor = db.cursor()
            cursor.execute("UPDATE tasks SET Pago=?, Data_pagamento=? WHERE Task=? AND Data_vencimento=?", (1, data_pagamento, name, data_vencimento_split))
            db.commit()

            cursor.close()

        firt_page.controls[1].controls[0] = calculate_value_paied()
        firt_page.controls[2].controls[0] = calculate_value()
        firt_page.update()
        e.controls[0].content.update()
    
    def mes_atual():
        import locale
        import datetime
        # Defina a localização para português do Brasil (pt_BR)
        locale.setlocale(locale.LC_TIME, 'pt_BR')

        # Obtenha a data atual
        data_atual = datetime.datetime.now()

        # Obtenha o nome do mês atual no formato em português
        mes_corrente = data_atual.strftime('%B').capitalize()


        return mes_corrente

    def AddTaskToScreen(e):
        


        # Defina a localização para português do Brasil (pt_BR)
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')



        if (form_add.content.controls[0].value 
            and form_add.content.controls[1].value
            and date_picker.value is not None):

            data_vencimento = date_picker.value
            data_vencimento_datetime = datetime.strptime(data_vencimento.strftime('%d/%m/%Y'), '%d/%m/%Y')
            data_vencimento = data_vencimento.strftime('%d/%m/%Y')


            if dropdown_mês.value is not None and dropdown_mês.value != "Todos Meses":
                mes_corrente = dropdown_mês.value
                # Converta a string dateTime em um objeto datetime
            else:
                mes_corrente = mes_atual()


            db = Database.ConnectToDatabase()

            first_data_vencimento = f"Vencimento: {data_vencimento}"

            data_atual = datetime.now()

            data_entrada = data_atual.strftime("%d/%m/%Y") 
                
            if form_add.content.controls[3].controls[0].value == False:
                # Inserção da primeira parcela no banco de dados
                Database.InsertDatabase(db, (
                    form_add.content.controls[0].value,
                    form_add.content.controls[1].value,
                    mes_corrente,
                    data_vencimento,
                    data_entrada
                ))
            else:
                mes_corrente = mes_atual()
                for i in range(12):
                    
                    # Calcula a nova data de vencimento adicionando 'i' meses à data de vencimento inicial
                    new_vencimento_datetime = data_vencimento_datetime + relativedelta(months=i)
                    # Formata a nova data de vencimento para uma string no formato desejado
                    new_data_vencimento = new_vencimento_datetime.strftime('%d/%m/%Y')
                    
                    # Calcula o novo mês adicionando o número da parcela ao mês atual
                    new_date = datetime.strptime("1 " + mes_corrente, "1 %B").replace(day=1) + relativedelta(months=i)
                    new_mes_corrente = new_date.strftime("%B").title()
                    
                    if new_mes_corrente == "Marã§O":
                        new_mes_corrente = "Março"
                    

                    # Insere no banco de dados com o novo mês corrente
                    Database.InsertDatabase(db, (
                        form_add.content.controls[0].value,
                        form_add.content.controls[1].value,
                        new_mes_corrente,
                        new_data_vencimento,
                        data_entrada
                    ))


            db.close()

        else:
            pass


        completename = f"{form_add.content.controls[0].value} R$ {form_add.content.controls[1].value}"
        color = "white"
        if (form_add.content.controls[0].value 
            and form_add.content.controls[1].value
            and date_picker.value is not None):
            firt_page.controls.append(
                Createtask(
                    completename,
                    first_data_vencimento,
                    color,
                    DeleteFunction,
                    UpdateFunction,
                    FinalFuncition,

                )
            )

            firt_page.controls[1].controls[0] = calculate_value_paied()
            firt_page.controls[2].controls[0] = calculate_value()
            firt_page.update()

            CreateToDoTask(e)

    def get_dropdown_value(e):
        value_dropdown = dropdown_mês.value

        # Crie uma lista temporária para armazenar os controles de Createtask a serem removidos
        controls_to_remove = []

        # Loop pelas instâncias de Createtask dentro de firt_page
        for controle in firt_page.controls:
            if isinstance(controle, Createtask):
                controls_to_remove.append(controle)

        # Remova os controles de Createtask da firt_page
        for controle in controls_to_remove:
            firt_page.controls.remove(controle)

        db = Database.ConnectToDatabase()

        if value_dropdown == "Todos Meses":

            for task in Database.ReadDatabase(db)[::-1]:
                data_vancimento_format = f"Vencimento: {task[4]}"
                price_str = task[1]
                pago = task[2]

                # Concatene o nome e o preço
                task_combined = f"{task[0]} R$ {price_str}"

                if pago == 1:
                    task_combined += " - PAGO"

                color = "green" if pago == 1 else "white"
                
                firt_page.controls.append(
                    Createtask(
                        task_combined,
                        data_vancimento_format,
                        color,
                        DeleteFunction,
                        UpdateFunction,
                        FinalFuncition,
                    )
                )
        
        else:
            for task in Database.ReadDatabase(db)[::-1]:
                data_vancimento_format = f"Vencimento: {task[4]}"
                if task[3] == value_dropdown:
                    price_str = task[1]
                    pago = task[2]

                    # Concatene o nome e o preço
                    task_combined = f"{task[0]} R$ {price_str}"

                    if pago == 1:
                        task_combined += " - PAGO"

                    color = "green" if pago == 1 else "white"

                    firt_page.controls.append(
                        Createtask(
                            task_combined,
                            data_vancimento_format,
                            color,
                            DeleteFunction,
                            UpdateFunction,
                            FinalFuncition,
                        )
                    )


        firt_page.controls[1].controls[0] = calculate_value_paied()

        firt_page.controls[2].controls[0] = calculate_value()

        if value_dropdown != "Todos Meses":
            firt_page.controls[0].controls[0].value = f"Contas de {value_dropdown}"
        else:
            firt_page.controls[0].controls[0].value = "Todas Contas"
        
        firt_page.update()
        restore(e)
        
    dropdown_mês = Dropdown(
                    label="Escolha o Mês",
                    label_style=TextStyle(color=colors.BLUE_200),
                    height=50,
                    width=200,
                    filled=True,
                    border_radius=10,
                    text_size=15,
                    border_color=colors.BLUE_200,
                    bgcolor="#1F2128",
                    value=mes_atual(),
                    on_change= get_dropdown_value,
                    options=[
                        dropdown.Option("Todos Meses"),
                        dropdown.Option("Janeiro"),
                        dropdown.Option("Fevereiro"),
                        dropdown.Option("Março"),
                        dropdown.Option("Abril"),
                        dropdown.Option("Maio"),
                        dropdown.Option("Junho"),
                        dropdown.Option("Julho"),
                        dropdown.Option("Agosto"),
                        dropdown.Option("Setembro"),
                        dropdown.Option("Outubro"),
                        dropdown.Option("Novembro"),
                        dropdown.Option("Dezembro"),

                    ],
                    
                        
                    )

    date_picker = DatePicker(
    )

    firt_page = Column(
        expand=True,
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.HIDDEN,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text(
                        f"Contas de {mes_atual()}", size=22, weight="bold", color="white"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=22,
                        on_click=lambda e: CreateToDoTask(e)
                        
                        ),
                    IconButton(
                        icons.MENU_ROUNDED,
                        icon_size=24,
                        on_click=lambda e: shrink(e)
                    ),       
                ],
            ),
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    calculate_value_paied()
                    ]
            ),
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    calculate_value()
                    ]
            ),


            Divider(height=8, color="white24")
        ]
    )

    main_column = Row(
        alignment="end",
        vertical_alignment=CrossAxisAlignment.CENTER,
        controls=[
            Container(
                    width=400,
                    height=700,
                    border_radius=20,
                    bgcolor= "#17181d",
                    padding=padding.only(top=20, left=20, right=20, bottom=5),
                    animate=animation.Animation(600, AnimationCurve.DECELERATE),
                    animate_scale= animation.Animation(400, AnimationCurve.DECELERATE),
                    clip_behavior=ClipBehavior.HARD_EDGE,
                    content=Column(
                        expand=True,
                        controls=[
                            firt_page,
                            FormContainer().build(),
                        ]
                    )
            )
        ]
    )
    #FINAL DAS FUNÇÕES E WIDGET DA 1 PAGINA.



    #INICIO DAS FUNÇÕES E WIDGET DA 2 PAGINA.
    second_page = Container(
                    width=400,
                    height=700,
                    border_radius=20,
                    bgcolor= "#17181d",
                    padding=padding.only(top=20, left=20, right=20, bottom=5),
                    animate=animation.Animation(600, AnimationCurve.DECELERATE),
                    animate_scale= animation.Animation(400, AnimationCurve.DECELERATE),
                    clip_behavior=ClipBehavior.HARD_EDGE,
                    content=Column(
                        controls=[
                        Row(
                        alignment="end",
                        controls= [
                            IconButton(icons.ARROW_BACK, icon_color= "white",on_click=lambda e: restore(e)),

                            ],
                        ),

                        Divider(height=20,color="transparent"),

                        Row(
                                alignment="Center",
                                controls=[
                                    Stack(
                                        controls=[
                                            AnimatedBox("#e9665a", None, 0),
                                            AnimatedBox("#7df6dd", "#23262a", pi / 4)

                                        ]

                                    ),

                                ]
                            ),


                        Divider(height=20,color="transparent"),


                        Row(
                            alignment="Center",
                            controls= [
                                Text("Olá, Théo", size=34,weight="bold",color="white"),
                            ],
                            
                        ),


                        Divider(height=20,color="transparent"),

                        Row(
                            alignment="Center",
                            controls=[
                                dropdown_mês
                            ]

                        ),
                        Divider(height=10,color="transparent"),

                        Row(
                            alignment="center",
                            controls=[
                                
                                TextButton(text="Wallet", icon=icons.WALLET_OUTLINED, on_click=lambda e: open_pg_3(e)),
                                
                            ]

                        ),
                        Divider(height=10,color="transparent"),
                        Row(
                            alignment="center",
                            controls=[
                                TextButton(text="Exportar Dados", icon=icons.DOWNLOAD_OUTLINED, on_click=lambda e: report(e))
                            ]

                        ),
                        Divider(height=10,color="transparent"),
                        
                        Row(
                            alignment="center",
                            controls=[
                                TextButton(text="Voltar", icon=icons.LOGIN_OUTLINED, on_click=lambda e: restore(e))
                            ]

                        )                          
                        ]
                    )
                
    )

    def open_pg_3(e):
        main_column.opacity = 0
        if second_page.height == 700:
            second_page.height = 0
            third_page.controls[0].height = 700

            second_page.update()
            third_page.update()
            firt_page.update
        main_column.update()

    def shrink(e):
        main_column.controls[0].width = 80
        main_column.controls[0].border = border.all(0.5, "white")
        main_column.controls[0].scale = transform.Scale(0.7, alignment=alignment.center_right)
        main_column.controls[0].border_radius=border_radius.only(
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        page.update()

    def restore(e):
        main_column.controls[0].width = 400
        main_column.controls[0].border = None
        main_column.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        main_column.controls[0].border_radius=border_radius.only(
            top_left=40,
            top_right=40,
            bottom_left=40,
            bottom_right=40
        )
        page.update()

    def report(e):

        connection = sqlite3.connect('finanças.db')
        query = "SELECT * FROM tasks"
        df = pd.read_sql_query(query, connection)
        connection.close()

        # Obtendo o caminho do diretório de downloads no Windows
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Especificando o caminho completo do arquivo CSV na pasta Downloads
        csv_file_path = os.path.join(downloads_folder, 'Dados_de_contas.csv')

        # Exportando o DataFrame para o arquivo CSV
        df.to_csv(csv_file_path, index=False)

        open_dlg(e)

    def animate_boxes():

        clock_wise_rotate = pi /4

        counter_clock_wise_rotate = -pi * 2

        red_box = contender.content.controls[0].content.controls[2].controls[0].controls[0].controls[0]
        blue_box = contender.content.controls[0].content.controls[2].controls[0].controls[1].controls[0]

        counter = 0

        while True:

            if counter >= 0 and counter <= 4:
                red_box.rotate = transform.Rotate(
                    counter_clock_wise_rotate, alignment.center

                )
                
                blue_box.rotate = transform.Rotate(
                    clock_wise_rotate, alignment.center

                )


                red_box.update()
                blue_box.update()


                clock_wise_rotate += pi / 2
                counter_clock_wise_rotate -= pi / 2
                
                counter += 1
                sleep(0.7)


            if counter >=5 and counter <= 10:
                
                clock_wise_rotate -= pi / 2
                counter_clock_wise_rotate += pi / 2

                red_box.rotate = transform.Rotate(
                    counter_clock_wise_rotate, alignment.center

                )
                
                blue_box.rotate = transform.Rotate(
                    clock_wise_rotate, alignment.center

                )

                red_box.update()
                blue_box.update()

                counter += 1
                sleep(0.7)

            if counter > 10:
                counter = 0
    
    dlg = AlertDialog(
        title= Text("Dados Exportados com Sucesso!", size=18)
    )
    
    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    #FINAL DAS FUNÇÕES E WIDGET DA 2 PAGINA



    #INICIO DAS FUNÇÕES E WIDGET DA 3 PAGINA
    def AddCardToSCreen(e):
        

        bank_name = form_card.content.controls[3].value
        card_number = form_card.content.controls[4].value
        card_cvc = form_card.content.controls[5].value 
        data = form_card.content.controls[6].value 

        card_number = card_number.replace(" ", "")

        grupos_de_4_digitos = [card_number[i:i+4] for i in range(0, len(card_number), 4)]

        card_number = " ".join(grupos_de_4_digitos)

        if bank_name and card_number and card_cvc:

            db = Database_card.ConnetToDatabase_card()
            Database_card.InsertDatabase(db,(bank_name, card_number, card_cvc, data))

            db.close()


        if bank_name and card_number and card_cvc:

            if form_card.height == 400:                
                form_card.height, form_card.opacity = 0, 0
                form_card.update()
            third_page.controls[0].content.controls.append(
                Column(
                    controls=[
                        Row(
                            alignment="center",
                            controls=[
                                    AddCard(
                                    bank_name,
                                    card_number,
                                    card_cvc,
                                    data
                                )
                            ]
                        )
                    ]
                )

            )
            


            third_page.update()
            page.update()

    def CreateCardTask(e):

        form_card.content.controls[7].on_click = lambda e: AddCardToSCreen(e)
        


        if form_card.height != 400:
            form_card.height, form_card.opacity = 400, 1
            form_card.update()

        else:
            
            form_card.height, form_card.opacity = 0, 0
            form_card.content.controls[3].value = None
            form_card.content.controls[4].value = None
            form_card.content.controls[5].value = None
            form_card.content.controls[6].value = None
            form_card.content.controls[7].content.value = "Adicionar"
            form_card.content.controls[7].on_click = lambda e: AddCardToSCreen(e)
            form_card.update()

    def restore_home(e):
            second_page.height = 700
            third_page.controls[0].height = 0
            main_column.opacity = 1

            page.update()

    third_page = Row(
        alignment="end",
        vertical_alignment=CrossAxisAlignment.CENTER,
        controls=[
            Container(
                width=400,
                height=0,
                bgcolor="#17181d",
                border_radius=20,
                padding=padding.only(top=50, left=20, right=20, bottom=5),
                animate=animation.Animation(600, AnimationCurve.DECELERATE),
                animate_scale= animation.Animation(400, AnimationCurve.DECELERATE),
                clip_behavior=ClipBehavior.HARD_EDGE,
                content=Column(
                    expand=True,
                    scroll="hidden",
                    controls=[
                            Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls= [
                                IconButton(icons.ARROW_BACK, icon_color= "white",on_click=lambda e: restore_home(e)),
                                Text("Wallet", color="white", size=32, weight="bold"),
                                IconButton(icon=icons.ADD_CARD_OUTLINED,icon_color="white",on_click=lambda e: CreateCardTask(e))
                                ],
                            ),
                            Divider(height=20, color="white24"),
                            FormCard().build()
                    ]
                )



            )
        ]
    )

    #INICIO PAGINA TITULO.
    
    data_atual = datetime.now()
    data_atual = data_atual.strftime("%d-%m-%Y")

    column_title =Row(
        alignment="center",
        controls=[
            Container(
                    width=400,
                    height=60,
                    border_radius=20,
                    bgcolor= "#17181d",
                    padding=padding.only(left=20, right=20, bottom=5),
                    content=Container(
                        content=Row(
                        alignment="spaceBetween",
                        expand=True,
                        controls=[
                            Row(
                                alignment="center",
                                controls=[
                                IconButton(icon=icons.ATTACH_MONEY, icon_size=30, icon_color="green"),
                                Text("Bills Control", color=colors.WHITE, size=22, weight="bold"),
                                ]
                            ),
                            Column(
                                alignment="center",
                                controls=[
                                    Text(data_atual , color=colors.WHITE, size=14, weight="bold")
                                ]
                            )
                            
                            
                        ]
                        )

                    )
            )
        ]
    )
    
    # FIM PAGINA TITULO


    contender = Container(
            width=400,
            height=700,
            content= Stack(
                controls=[
                    second_page,
                    third_page,
                    main_column,
                    
                ]
            )
            
            )


    form_add = main_column.controls[0].content.controls[1]
    form_card = third_page.controls[0].content.controls[2]

    
    page.overlay.append(date_picker)
    
    
    page.add(
        column_title,
        Row(
            expand=True,
            controls=[
                contender,

            ]
        ),
        

        )
    page.update()

    # Inserido contas salvas no DB ao inciar a aplicação
    db = Database.ConnectToDatabase()
    for task in Database.ReadDatabase(db)[::-1]:
        data_vancimento_add = f"Vencimento: {task[4]}"
        if task[3] == mes_atual():
            price_str = task[1]
            pago = task[2]

            # Concatene o nome e o preço
            task_combined = f"{task[0]} R$ {price_str}"

            if pago == 1:
                task_combined += " - PAGO"
            

            color = "green" if pago == 1 else "white"

            firt_page.controls.append(
                Createtask(
                    task_combined,
                    data_vancimento_add,
                    color,
                    DeleteFunction,
                    UpdateFunction,
                    FinalFuncition,
                )
            )
    firt_page.update()




        #Inserido Cartões ao salvos no DB ao iniciar a aplicação
    db_card = Database_card.ConnetToDatabase_card()
    for card in Database_card.ReadDatabase(db_card):

        CardName = card[0]
        CardNumber = card[1]
        CVCNumber = card[2]
        data = card[3]


        third_page.controls[0].content.controls.append(
                Column(
                    controls=[
                        Row(
                            alignment="center",
                            controls=[
                                    AddCard(
                                    CardName,
                                    CardNumber,
                                    CVCNumber,
                                    data
                                )
                            ]
                        )
                    ]
                )

            )
        
        third_page.update()
        page.update()



    # Crie uma instância da thread
    animation_thread = threading.Thread(target=animate_boxes)

    # Inicie a thread
    animation_thread.start()
    

app(target=main)