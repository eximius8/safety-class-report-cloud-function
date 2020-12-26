from pylatex import Document, Section, MiniPage, Command, Package, MultiColumn, Section
from pylatex.table import Tabu

from pylatex.utils import bold, NoEscape
from pylatex.basic import LineBreak
from pylatex.math import Math

from bibliog import Bibliogr


class WasteReport(Document):

    def __init__(self, data_dict):
        geometry_options = {"left": "20mm", "right": "20mm", "top": "8mm", "bottom": "20mm"}
        super().__init__('basic',geometry_options=geometry_options)      
        
        

        self.name = data_dict['name']
        self.fkko = data_dict['fkko']
        self.k = data_dict['total_k']
        self.safety_class = data_dict['safety_class']
        self.components = data_dict['components']

        self.props = {}
        self.litsources = {}

        self.documentclass = Command(
                        'documentclass',
                        options=['12pt',],
                        arguments=['article'],
                    )


    def create_preamble(self):

        # packages
        self.packages.append(Package(name='fontenc', options="T2A"))
        self.packages.append(Package(name='inputenc', options="utf8"))
        self.packages.append(Package(name='babel', options="russian"))
        self.packages.append(Package(name='fixltx2e'))
        self.packages.append(Package(name='titlesec'))
        self.packages.append(Package(name='lmodern'))
        
        # preamble
        self.preamble.append(NoEscape(r"\titleformat{\section}[block]{\Large\bfseries\filcenter}{}{1em}{}"))
        self.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.5}"))
        # bibliography
        
    
    def create_head(self, param, value):
        
        with self.create(MiniPage(width=r"0.27\textwidth")):
            self.append(param)
            
        with self.create(MiniPage(width=r"0.68\textwidth")):
            self.append(bold(value))   
    
    def create_comp_table(self):

        self.append(LineBreak())
        self.append(Command("scriptsize"))
        total_concp = 0
        has_known_components = False # flag that the waste has components
        #has_soil_components = False  
        

        with self.create(Tabu(r"|X[2.2]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|", to=r"\textwidth", width=8)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Компонент",
                                "Сод., \%",
                                "$C_i$, мг/кг",
                                "$X_i$",
                                "$Z_i$",
                                "$\lg W_i$",
                                "$W_i$, мг/кг",
                                "$K_i$"], 
                                #mapper=bold,
                                color="gray", escape=False)
            data_table.add_hline()
            for compnt in self.components:
                concp = float(compnt['concp'])
                concr = float(compnt['concr'])
                k = float(compnt['k'])
                name = compnt['component']['name']
                x = compnt['component']['get_x']
                z = compnt['component']['get_z']
                log_w = compnt['component']['get_log_w']
                w = compnt['component']['get_w']
                 
                x_lit_source = compnt['component']['x_value_lit_source']
                binf = compnt['component']['Binf']
                if compnt['component']['props']:
                    self.props[name] = compnt['component']['props']
                    
              #  land_concentration = compnt['component']['land_concentration']
               # land_concentration_lit_source = compnt['component']['land_concentration_lit_source']

                 
                if x_lit_source:
                    name = NoEscape(name + r"\footnotemark[1]")                    
                    has_known_components = True                
               # elif val['has_soil_c']:
               #     key2 = NoEscape(key + r"\footnotemark[2]")
               #     if has_soil_components:
               #         key2 =  NoEscape(key + r"\footnotemark[2]")
               #     has_soil_components = True
               # else:
               #     key2=key
 
              
                data_table.add_row([name,
                                    "%.2f" % concp,
                                    "%.0f" % concr, 
                                    "%.2f" % x, 
                                    "%.2f" % z, 
                                    "%.2f" % log_w, 
                                    "%.0f" % w, 
                                    "%.1f" % k])
                total_concp += concp
      
                data_table.add_hline()                

            
            data_table.add_row(( "Компонентов учтено", "%.0f" % total_concp + " %", MultiColumn(6, align='r|', data='')))
            data_table.add_hline()    
            data_table.add_row([MultiColumn(7, align='|r|', data='Показатель К степени опасности отхода:'), "%.1f" % self.k])
            data_table.add_hline()
            data_table.add_row(( MultiColumn(7, align='|r|', data='Класс опасности отхода:'), self.safety_class))
            data_table.add_hline() 

        if has_known_components:
            self.append(NoEscape(r"\footnotetext[1]{Данные приведены согласно приказу Министерства природных ресурсов и экологии РФ от 4 декабря 2014 г. N 536}"))
     #   if has_soil_components:
    #        self.append(NoEscape(r"\footnotetext[2]{Концентрация не превышает содержание в основных типах почв, принято W=10\textsuperscript{6} (МПР 536)}"))


        self.append(Command("normalsize"))
        self.append(Command("bigskip"))    
        self.append(LineBreak())

    def fill_document(self):
        """Add a section, a subsection and some text to the document."""
        self.append(Section('Протокол расчета класса опасности отхода'))
        self.create_head("Наименование отхода:", self.name)        
        self.append(Command("bigskip"))
        self.append(LineBreak()) 
        if self.fkko:
            self.create_head("Код ФККО:", self.fkko)
            self.append(Command("bigskip"))
            self.append(LineBreak())
        self.append("Расчет класса опасности отхода выполнен в соответствии с \
        <<Критериями отнесения отходов к I-V классам опасности по степени негативного воздействия на окружающую среду>>, \
        утвержденными приказом МПР России от 04 декабря 2014 г. № 536.")

        self.append(Command("bigskip"))
        self.append(Command("noindent"))

        self.create_comp_table()        
        

        self.append("Показатель ")
        self.append(Math(data="K", inline=True))
        self.append(" степени опасности отхода для окружающей среды рассчитывается по следующей формуле:")
        self.append(Math(data="K=K_1+K_2+\dots +K_n,", escape=False))
        self.append("где ")
        self.append(Math(data="K_1, K_2, \ldots, K_n", inline=True, escape=False))
        self.append(NoEscape(" --- показатели степени опасности отдельных компонентов отхода для окружающей среды, "))
        
        self.append(Math(data=" n ", inline=True))
        self.append(NoEscape(" --- количество компонентов отхода."))
        self.append(LineBreak())
        self.append("Отнесение отходов к классу опасности расчетным методом по показателю\
         степени опасности отхода для окружающей среды осуществляется в соответствии с таблицей:")

        self.append(LineBreak())
        self.append(Command("bigskip"))
        self.append(LineBreak())
        self.append(Command("noindent"))

        with self.create(Tabu(r"|X[c]|X[c]|", to=r"\textwidth", width=2)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Класс опасности отхода",
                                "Степень опасности 	отхода для окружающей среды"], 
                                mapper=bold,
                                color="lightgray")
            data_table.add_hline()
            data_table.add_row(["I", "$10^4 \leq  K < 10^6 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["II", "$10^3 \leq  K < 10^4 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["III", "$10^2 \leq   K  < 10^3 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["IV", "$10 < K < 10^2 $"], escape=False)
            data_table.add_hline()


            data_table.add_row(["V", "$K \leq 10 $"], escape=False)
            data_table.add_hline()
        self.append(Command("bigskip"))
        self.append(LineBreak())

        self.append(NoEscape(r"""Степень опасности компонента отхода для окружающей среды $K_i$
        рассчитывается как отношение концентрации компонента отхода $C_i$ к коэффициенту его степени опасности для окружающей среды $W_i$:
        $$K_i = \frac{C_i}{W_i},$$
        где	$C_i$ --- концентрация $i$--тогo компонента в отходе [мг/кг]; 
         $W_i$ --- коэффициент степени опасности $i$-того компонента отхода для окружающей среды, [мг/кг].
        """)) 
        
        self.append(LineBreak())
        self.append("""Для определения коэффициента степени опасности компонента отхода \
         для окружающей среды по каждому компоненту отхода устанавливаются степени их \
         опасности для окружающей среды для различных компонентов природной среды.""")
        self.append(LineBreak())

        for name, props in self.props.items():            
            self.print_component_data(name, props)         


        self.create_bibliography()

        self.append(Command("bigskip"))
        self.print_shortcuts() 
        

    
    def print_component_data(self, name, props):
        self.append(LineBreak())
        self.append(f'Первичные показатели опасности компонента: {name}')
        self.append(LineBreak())
        self.append(LineBreak())
        self.append(Command("scriptsize"))
        if len(props) < 6:
            Binf = 1
        elif 6 <= len(props) <= 8:
            Binf = 2
        elif 8 < len(props) <= 10:
            Binf = 3
        else:
            Binf = 4
        with self.create(Tabu(r"|X[3]|X[c]|X[c]|X[c]|", to=r"\textwidth", width=4)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Показатель опасности",
                                "Значения показателя",
                                "Балл",
                                "Источник информации"], 
                                mapper=bold,
                                color="lightgray")
            data_table.add_hline()
           
            for prop in props:
                sources = ""
                for litsource in prop['literature_source']:
                    self.litsources[litsource['name']] = litsource['latexpart']
                    sources +=  "\\" + f'cite{{{litsource["name"]}}}' 


                data_table.add_row([prop['name'], prop['value'], prop['score'], NoEscape(sources)]) 
                data_table.add_hline()
            data_table.add_row(("Показатель информационного обеспечения",  MultiColumn(3, align='l|', data=Math(data=f"Binf={Binf}", inline=True))))
            data_table.add_hline()
        self.append(Command("normalsize"))        
        self.append(LineBreak())

    
    def create_bibliography(self):
        if self.litsources:
            with self.create(Bibliogr(arguments="9")) as environment:            
                for name, latexp in self.litsources.items():   
                    environment.append(Command('bibitem',name))
                    environment.append(NoEscape(latexp))
                    #self.append(LineBreak())   
    





    def print_shortcuts(self):
        """
        Печать сокращений
        """
        self.append(Section(title="Перечень сокращений"))
        sokrashen = {"ПДКп, мг/кг": "Предельно допустимая концентрация вещества в почве",
                     "ОДК, мг/кг": "Ориентировочно допустимая концентрация",
                     "ПДКв, мг/л": "Предельно допустимая концентрация вещества в воде водных объектов, используемых для целей питьевого и хозяйственно-бытового водоснабжения",
                     "ОДУ, мг/л": "Ориентировочно допустимый уровень",
                     "ОБУВ, мг/л": "Ориентировочный безопасный уровень воздействия",
                     "ПДКр.х., мг/л": "Предельно допустимая концентрация вещества в воде водных объектов рыбохозяйственного значения",
                     r"ПДКс.с., мг/м\textsuperscript{3}": "Предельно допустимая концентрация вещества среднесуточная в атмосферном воздухе населенных мест",
                     "ПДКп.п.": "Предельно допустимая концентрация вещества в пищевых продуктах",
                     r"ПДКм.р., мг/м\textsuperscript{3}": "Предельно допустимая концентрация вещества максимально разовая в атмосферном воздухе населенных мест",
                     r"ПДКр.з., мг/м\textsuperscript{3}": "Предельно допустимая концентрация вещества в атмосферном воздухе рабочей зоны",
                     "МДС, мг/кг": "Максимально допустимое содержание",
                     "МДУ, мг/кг": "Максимально допустимый уровень",
                     r"$S$, мг/л": "Растворимость компонента отхода (вещества) в воде при 20°С",
                     r"С\textsubscript{нас}": "Насыщающая концентрация вещества в воздухе при 20°С и нормальном давлени",
                     r"$K_{ow}$": "Коэффициент распределения в системе октанол/вода при 20°С",
                     r"LD\textsubscript{50}": "Средняя смертельная доза компонента в миллиграммах действующего вещества на 1 кг живого веса, вызывающая гибель 50% подопытных животных при однократном пероральном введении в унифицированных условиях",
        }
        with self.create(Tabu(r"|X[c]|X[2]|", to=r"\textwidth", width=2)) as data_table:
            data_table.add_hline()
            for name, data in sokrashen.items():
                data_table.add_row(NoEscape(name), data)             
                data_table.add_hline()
            



        
        
        