from tkinter import *  # Importera alla funktioner och metoder från tkinters biblotek utan att importera dem implicit.
# Importerar messagebox från tikinter som meddelande, kan nu skapa messagebox
from tkinter import messagebox as meddelande
import random  # Används för att slumpa listor

"""Konstanter, dessa variabelers värde kommer inte ändras"""
BAKGRUNDSFÄRG = "#FFBE6A"  # Bakgrundsfärgen för spelet
FÖNSTER_STORLEK = "700x600"  # Storleken på fönstret, breddxhöjd
KNAPPFÄRG = "#FF847C"  # Färgen på "vanliga" knappar
# En lista med alla fönstertyper
FÖNSTERTYP = ["Välkommen till Memory", "Regler", "Spel Inställningar", "Memory", "Highscore Lista"]


def skapa_nya_fönster(fönster_typ):
    """
    Funktionen används för att skapa ett nytt fönster och beroende på parametern, kommer den
    specifika fönster typen att skapas med hjälp av de olika klasserna som kallas
    """

    fönster_namn = fönster_typ  # Lagrar parametern i variabeln.
    ny_fönster = Toplevel()  # Skapar ett fönster.

    # If-satserna granskar vilket fönster som ska skapas.
    if fönster_namn == FÖNSTERTYP[1]:
        ReglerFönster(ny_fönster, fönster_namn)  # Klassen "ReglerFönster" anropas, beskriver reglerna
    elif fönster_namn == FÖNSTERTYP[2]:
        # Klassen "SpelInställningarFönster" anropas, tar hand om inställningar
        SpelInställningarFönster(ny_fönster, fönster_namn)
    elif fönster_namn == FÖNSTERTYP[3]:
        # Variabeln fönster_namn och ny_fönster returneras, kommer användas vid anropandet av klassen "SpelFönster"
        return ny_fönster, fönster_namn
    elif fönster_namn == FÖNSTERTYP[4]:
        # Variabeln fönster_namn och ny_fönster returneras, kommer användas vid anropandet av klassen "HighscoreFönster"
        return ny_fönster, fönster_namn


class FönsterEgenskaper:
    """
    Standard egenskaper för alla fönster som skapas, klassen kommer att ärvas.
    """

    def __init__(self, fönster, titel):
        """
        Alla nedanstående attribut är gemensamma för alla fönster som skapas. Parametrarna som tas in är ett fönster och
        den specifika titeln för fönstret.
        """
        self.fönster = fönster  # Typen av fönster lagras i self.fönster
        self.fönster_namn = titel  # Den specifika titeln lagras för fönstret
        self.ikon = PhotoImage(file='Memory.png')  # Lägger till ikonbild för fönster
        self.fönster.config(bg=BAKGRUNDSFÄRG)  # Ändrar fönstrets bakgrundsfärg till en specifik färg
        self.fönster.iconphoto(True, self.ikon)  # Byter ut den gamla icoen med den nya
        self.fönster.geometry(FÖNSTER_STORLEK)  # Anpassar fönstrets storlek
        self.fönster.title(self.fönster_namn)  # Den specifika titeln appliceras för fönstret

    def avsluta(self):  # Gemensamma egenskaper för alla fönster som öppnas/skapas
        """
        Används vid stängning av fönster
        :return:
        """

        def stäng_fönster():
            """
            När spelaren ska stänga fönster, skapas en messagebox som bekräftar om den verkligen vill avsluta fönster,
            om knappen "ja" trycks kommer detta vara "True" och fönstrerna kommer att avslutas
            """
            if meddelande.askyesno(title="Avsluta", message="Vill du avsluta?"):
                self.fönster.quit()  # Avslutar programmet.

        # "WM_DELETE_WINDOW" detekterar att fönstret stängs, anropar på funktionen "stäng_fönster"
        self.fönster.protocol("WM_DELETE_WINDOW", stäng_fönster)


class StartsidaFönster(FönsterEgenskaper):
    """Klassen gör fönstret till en startsida som välkomnar spelaren"""

    def __init__(self, fönster, titel):
        super().__init__(fönster, titel)  # Klassen får tillgång till "FönsterEgenskaper" attribut samt klass metoder
        # Lagrar en bild, bildfilen finns i samma mapp därför behövs ingen path anges.
        self.bild = PhotoImage(file='Memory.png')

        # Labeln som skapas ska vara rubriken för startsidan
        self.rubrik = Label(fönster,  # Fönstret där labeln visas
                            text="Välkommen till Memory",  # Texten för rubriken
                            font=('Arial', 21, 'bold'),  # Typsnittet för rubriken
                            image=self.bild,  # Bilden ska nu visas tillsammans med rubriken
                            compound='top',  # Visar bilden ovanför rubriken
                            bg=BAKGRUNDSFÄRG)  # Bakgrundsfärgen för rubriken
        self.rubrik.pack()  # Lägger till rubriken i fönstret, längst upp.

        # Knappen som skapas ska ta spelaren vidare till ett annat fönster som beskriver reglerna för spelet
        self.gå_till_menyn = Button(fönster,
                                    text="Gå Vidare",  # Texten på knappen
                                    font=('Arial', 20, 'bold'),  # Typsnittet för texten
                                    relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                    bd=5,  # Boardens storlek
                                    bg=KNAPPFÄRG,  # Färgen på knappen
                                    activebackground=KNAPPFÄRG,  # Vid klickning av knappen kommer färgen vara detsamma
                                    command=self.gå_vidare)  # Metoden körs vid användning av knappen

        # Lägger till knappen i fönstret, både "side" och "pady" positionerar knappen
        self.gå_till_menyn.pack(side=BOTTOM, pady=50)

        FönsterEgenskaper.avsluta(self)  # Anropar på en klass metod som ska felhantera avslutning av ett fönster

    def gå_vidare(self):
        """
        Gömmer den "nuvarande" fönstret och öppnar ett nytt fönster
        """
        self.fönster.withdraw()  # Gömmer Startsidans fönster
        skapa_nya_fönster(FÖNSTERTYP[1])  # Skapar ett nytt fönster


class ReglerFönster(FönsterEgenskaper):
    """
    Klassen Regler presenterar reglerna för spelet med hjälp av en label
    """

    def __init__(self, fönster, fönster_titel):
        # Klassen får tillgång till "FönsterEgenskaper" attribut samt klass metoder
        super().__init__(fönster, fönster_titel)
        # Skapar en frame
        self.frame = Frame(self.fönster,  # Fönstret där framen är
                           relief=RAISED,  # Skapar en Boarder av typen "RAISED"
                           bg=BAKGRUNDSFÄRG)  # Bakgrundsfärgen för framen
        self.frame.place(relx=0.5, rely=0.4, anchor=CENTER)  # Framens placering
        # Skapar rubriken för regler
        self.rubrik = Label(self.frame,  # Rubriken ska visas i framen
                            text="REGLER",  # Rubrikens namn
                            relief=RAISED,  # Skapar en Boarder av typen "RAISED"
                            bd=10,  # Storleken för Boardern
                            font=('Arial', 40, 'bold'),  # Typsnittet för rubriken
                            bg=BAKGRUNDSFÄRG)  # Bakgrundsfärgen för rubriken
        # En label som presenterar reglerna skapas
        self.spelets_regler = Label(self.frame,  # Labeln ska visas i framen
                                    # Texten är reglerna
                                    text="Spelet går ut på att samla alla par med olika ord."
                                         "\nSpelaren får trycka på två valfria knappar, ett i taget."
                                         "\nOm det är olika ord göms orden på samma ställe."
                                         "\nOm det är samma ord så blir dessa ord synliga under spelets gång."
                                         "\nSpelaren fortsätter tills den fått alla matchningar."
                                         "\nResultatet sparas sedan,\n så se till att få alla rätt på så få försök som"
                                         " möjligt!",
                                    bd=5,  # Storleken för boardern som skapas
                                    font=('Consolas', 12),  # Typsnittet för labeln
                                    relief=GROOVE,  # Skapar en boarder för labeln av typen "SUNKEN"
                                    bg=BAKGRUNDSFÄRG)  # Bakgrundsfärgen för labeln

        self.knapp_fortsätt = Button(self.frame,  # Knappen ska visas i framen
                                     text="Fortsätt",  # Text för knapp
                                     bg=KNAPPFÄRG,  # Färgen för knappen
                                     activebackground=KNAPPFÄRG,  # Färgen är detsamma under klick av knapp
                                     command=self.fortsätt,  # Anropar metoden "fortsätt()" vid klickning
                                     font=('Arial', 20, 'bold'),  # Typsnittet för knapptexten
                                     bd=5)  # Storleken för knappens boarder som är av typen "RAISED"

        self.rubrik.pack(pady=20)  # Rubriken lägss till i fönstret och visas i framen
        self.spelets_regler.pack(pady=15)  # Labeln lägss till i fönstret och visas i framen
        self.knapp_fortsätt.pack(pady=10)  # Knappen lägss till i fönstret och visas i framen

        FönsterEgenskaper.avsluta(self)  # Anropar på en klass metod som ska felhantera avslutning av ett fönster

    def fortsätt(self):
        """
        Metoden gömmer det nuvarande fönstret och anropar på funktionen "skapa_nya_fönster()" för att gå vidare till
        spelinställningar.
        """
        self.fönster.withdraw()  # Gömmer fönstret
        skapa_nya_fönster(FÖNSTERTYP[2])  # Skapar ett nytt fönster


class SpelInställningarFönster(FönsterEgenskaper):
    """
    Klassen SpelInställningar justerar spelet utifrån spelarens val. Klassen registrerar spelarnamnet och storleken
    på den matris som spelaren vill spela i. Dessa val sparas och används i klassen SpelFönster(). De val som
    spelaren gör angående spelarnamn och matrisens storlek felhanteras.
    """

    def __init__(self, fönster, fönster_titel):
        # Klassen får tillgång till "FönsterEgenskaper" attribut samt klass metoder
        super().__init__(fönster, fönster_titel)
        # En LabelFrame skapas, alltså en rubrik för själva frame skapas
        self.frame = LabelFrame(self.fönster,  # Fönstret där framen är
                                bg=BAKGRUNDSFÄRG,  # Bakgrundsfärgen för rubriken
                                text="Spel Inställningar",  # Rubrikens text
                                font=('Arial', 20, 'bold'),  # Typsnittet för texten
                                pady=10)  # Placering av rubriken

        self.frame.place(relx=0.5, rely=0.4, anchor=CENTER)  # Placering av framen

        # En label för spelarnamn
        Label(self.frame,  # Labeln ska visas i framen
              text="Spelarnamn:",  # Texten för labeln
              font=('Arial', 12, 'bold'),  # Typsnittet för texten
              # Bakgrundsfärgen för labeln
              bg=BAKGRUNDSFÄRG).grid(row=0, column=0, pady=15)  # Placeringen av labeln rad- samt kolumnvis
        # En label för brädstorlek
        Label(self.frame,  # Labeln ska visas i framen
              text="Brädstorlek:",  # Texten för labeln
              font=('Arial', 12, 'bold'),  # Typsnittet för texten
              # Bakgrundsfärgen för labeln
              bg=BAKGRUNDSFÄRG).grid(row=1, column=0, pady=15)  # Placeringen av labeln rad- samt kolumnvis

        self.spelar_namn_textbox = Entry(self.frame,  # Textboxen ska visas i framen
                                         font=('Arial', 12, 'bold'))  # Typsnittet för textboxen
        self.spelar_namn_textbox.grid(row=0, column=1, padx=10, pady=15)  # Placeringen av textboxen rad- samt kolumnvis
        self.angiven_matris_textbox = Entry(self.frame,  # Textboxen ska visas i framen
                                            font=('Arial', 12, 'bold'))  # Typsnittet för textboxen

        self.angiven_matris_textbox.grid(row=1, column=1, padx=10, pady=15)  # Placering av textbox rad- samt kolumnvis
        # Skapar en knapp
        self.registrera_knapp = Button(self.frame,  # Knappen ska visas i framen
                                       text="REGISTRERA",  # Texten för knappen
                                       font=('Arial', 20, 'bold'),  # Typsnittet för knapptexten
                                       bg=KNAPPFÄRG,  # Färgen på knappen
                                       activebackground=KNAPPFÄRG,  # Färgen ändras inte trots att man klickar på den
                                       relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                       bd=5,  # Storleken för boardern
                                       # Anropar på metoden "registrera_felhantering", vid klick
                                       command=self.registrera_felhantering)
        # Placerar knappen
        self.registrera_knapp.grid(row=3,
                                   column=0,
                                   columnspan=2,
                                   pady=25,
                                   padx=15)

        FönsterEgenskaper.avsluta(self)  # Anropar på en klass metod som ska felhantera avslutning av ett fönster

    def inaktivera(self):
        """Inaktiverar allt som har med registreringen att göra, på så vis kan inte användaren trycka eller redigera
        sina val förrens spelaren tryckt på "ok" knappen som visas av en messagebox"""
        self.registrera_knapp['state'] = 'disabled'  # Inaktiverar knappen
        self.registrera_knapp['background'] = 'Grey'  # Ändrar bakgrundsfärgen för knappen till grått
        self.spelar_namn_textbox['state'] = 'disabled'  # Inaktiverar textboxen där man fyller i sitt spelarnamn
        self.angiven_matris_textbox['state'] = 'disabled'  # Inaktiverar textboxen där man fyller i matrisens storlek

    def aktivera(self):
        """Aktiverar allt som har med registreringen att göra, på så vis kan nu användaren trycka eller redigera
        sina val efter att ha tryckt på "ok" knappen som visas av en messagebox"""
        self.registrera_knapp['state'] = 'normal'  # Aktiverar knappen
        self.registrera_knapp['background'] = KNAPPFÄRG  # Ändrar bakgrundsfärgen för knappen till standardfärgen
        self.spelar_namn_textbox['state'] = 'normal'  # Aktiverar textboxen där man fyller i sitt spelarnamn
        self.angiven_matris_textbox['state'] = 'normal'  # Aktiverar textboxen där man fyller i matrisens storlek

    def messagebox(self):
        """Metoden anropas då använder skrivit in fel vid registrering av namn och matrisstorlek. Denna metod skapar en
        messagebox som informerar användaren om att spelaren skrivit fel. Här anropas även "aktivera()" och
        "inaktivera()" metoderna"""
        self.inaktivera()  # Metoden "inaktivera()" anropas och körs
        meddelande.showwarning(title='WARNING',  # Titeln för messageboxen
                               message="Du måste skriva matrisstorlek AxA form som är jämn! "
                                       "Du måste skriva in ett namn! " + "Högsta matrisen är 18x18 samt lägsta 2x2")
        self.aktivera()  # Metoden "aktivera()" anropas och körs

    def registrera_felhantering(self):
        """Metoden som anropas när man trycker på registrera knappen. Agerar som en felhantering vid inskrivning av
        spelarnamn samt matrisstorlek. Denna metod anropar funktionen "registrera" om inmatningen var okej, annars
        kallas en messagebox som visar att det man skrivit är fel och spelaren blir tvungen att skriva om.
        """
        # Tar det som är skrivet i textboxen vid knapptryck och lagrar texten som en sträng i variabeln "spelar_namn"
        spelar_namn = self.spelar_namn_textbox.get()

        """ Tar det som är skrivet i textboxen vid knapptryck och lagrar texten som en sträng i variabeln 
        angiven_matris och gör hela stängen till stora bokstäver, förutom siffrorna naturligtvis"""
        angiven_matris = self.angiven_matris_textbox.get().upper()

        # Kollar ifall spelarnamnet inte är tom eller består av space samt att den angivna matrisen har ett "X"
        if spelar_namn != "" and angiven_matris.__contains__("X") and not spelar_namn.__contains__(" "):
            # Variabeln slut_position används som referens för att få siffrorna inbakat i den angivna matrisen
            bokstav_position = int(angiven_matris.find("X"))
            # Den första siffran i den angivna matrisen lagras i variabeln "rad_storlek" och ska vara storleken på raden
            rad_storlek = angiven_matris[0: bokstav_position]
            # Andra siffran i den angivna matrisen lagras i variabeln "kolon_storlek" och ska vara storleken på kolonen
            kolonn_storlek = angiven_matris[bokstav_position + 1:]
            # If-satsen kollar ifall den första och andra siffran i matrisen är siffror eller om det är text
            if rad_storlek.isdigit() and kolonn_storlek.isdigit():
                rad_storlek = int(rad_storlek)  # Gör siffran i rad_storlek till integer istället för sträng
                kolonn_storlek = int(kolonn_storlek)  # Gör siffran i kolon_storlek till integer istället för sträng
                #  Om den angivna matrisen är större eller mindre än största respektiv minsta matrisen som kan skapas
                if (rad_storlek > 18 and kolonn_storlek > 18) or (rad_storlek < 2 and kolonn_storlek < 2):
                    self.messagebox()  # Anropar metoden "messagebox()"
                else:
                    #  Ifall rad_storlek och kolon_storlek är samma värde samt om de siffrorna är jämna.
                    if rad_storlek == kolonn_storlek and (rad_storlek % 2) == 0 and (kolonn_storlek % 2) == 0:
                        vald_storlek = rad_storlek  # rad_storleken läggs till i en tillfällig variabel "vald_storlek"
                        # "vald_storlek", "spelar_namn" är attribut som blir till "registrera()" metodens parametrar
                        self.registrera(vald_storlek, spelar_namn)
                    else:
                        self.messagebox()  # Anropar metoden "messagebox()"

            else:
                self.messagebox()  # Anropar metoden "messagebox()"

        else:
            self.messagebox()  # Anropar metoden "messagebox()"

    def registrera(self, vald_storlek, spelar_namn):
        """
        Denna metod använder parametrarna både spelarnamn och den valda matrisstorleken och skickar dessa variabler som argument
        tillsammans med andra argument för SpelFönster klassen.
        """

        """ 
        De returnerade variablerna från "skapa_nya_fönster()" funktionen lagras i ny_fönster respective fönster_namn.
        Dessa variabler tillsammans med "vald_storlek" och "spelar_namn" blir argument till parametrarna för klassen
        "SpelFönster()"
        """
        ny_fönster, fönster_namn = skapa_nya_fönster(FÖNSTERTYP[3])
        SpelFönster(vald_storlek, spelar_namn, ny_fönster, fönster_namn)  # Klassen "SpelFönster()" anropas
        self.fönster.withdraw()  # Det nuvarande fönstret göms


class SpelFönster(FönsterEgenskaper):
    """
    Klassen har metoder som alla utgör spelets alla funktioner. Spel-knapparna skapas samt placeras här. Efter att
    spelaren matchat alla ord med varandra kommer denna klass anropa på klassen SparaResultat för att spara spelarens
    resultat i en fil
    """

    def __init__(self, vald_storlek, spelar_namn, fönster, titel):
        # Klassen får tillgång till "FönsterEgenskaper" attribut samt klass metoder
        super().__init__(fönster, titel)
        self.spara_ny_fil_knapp = None  # Knappen ska spara resultatet i en highscorelista
        # Labeln ska visa antal rätta matchningar som spelaren gör, texten kommer alltså att uppdateras för varje runda
        self.antal_fel_text = None
        # Labeln ska visa antal rätta matchningar som spelaren gör, texten kommer alltså att uppdateras för varje runda
        self.antal_rätt_text = None
        self.match_eller_ej = None  # En label som anger om det blev en matchning eller inte
        # En lista som kommer att spara knapp objekt, objekten kommer att ha samma metod "knapp_tryck"
        self.knapp_objekt_lista = []
        self.ord_lista = []  # En lista som sparar ord från filen "vanliga.txt" med hjälp av funktioen "öppna_fil_ord"
        self.antal_rader = int(vald_storlek)  # Lagrar antalet rader, kommer användas för att göra "grid" på knapparna
        # Lagrar antalet koloner, kommer användas för att göra "grid" på knapparna
        self.antal_kolumner = int(vald_storlek)
        self.antal_valda_knappar = 0  # Håller koll på om spelaren har valt två knappar eller inte
        self.valda_knappar_lista = []  # En lista som håller koll på vilka knappar som trycks
        self.rätt_svar = []  # Sparar alla rätta matchningar, denna lista kommer användas vid felhantering av knappar
        self.antal_rätt = 0  # Antalet rätta matchningar
        self.antal_fel = 0  # Antalet försök
        self.spelar_namn = spelar_namn  # Namnet på spelaren
        self.frame = Frame(fönster)  # En frame för spel-knapparna
        self.frame_label_knapp = Frame(fönster, bg=BAKGRUNDSFÄRG)  # Frame för labels och knappar
        self.knapp_namn = []  # Lagrar varje knapp som namn, används till att referera till en specifik knapp
        FönsterEgenskaper.avsluta(self)  # Anropar på en klass metod som ska felhantera avslutning av ett fönster
        self.skapa_placera_knappar_labels()  # Anropar på metoden "placera_knappar_labels"

    def skapa_placera_knappar_labels(self):
        """
        Skapar och placerar alla knappar/labels i fönstret. Anropar även metoderna: "öppna_fil_ord" och
        "justerar_knapp_position"
        """
        self.frame.pack(pady=15)  # Placerar framen på en specifik y-koordinat, dock är x-koordinaten oförändrad
        self.frame_label_knapp.pack(side=TOP, pady=5)
        # En label som anger om det blev en matchning eller inte
        self.match_eller_ej = Label(self.frame_label_knapp,  # Fönstret där labeln visas
                                    text="",  # Texten på labeln, ingenting för tillfälligt då den ska uppdateras
                                    bg=BAKGRUNDSFÄRG,  # Bakgrundsfärgen för labeln.
                                    font=('Consolas', 14))  # Typsnittet för texten
        # Labeln ska visa antal rätta matchningar som spelaren gör, texten kommer alltså att uppdateras för varje runda
        self.antal_rätt_text = Label(self.frame_label_knapp,  # Fönstret där labeln visas
                                     text="Antal Rätt: " + str(self.antal_rätt),  # Texten på label, uppdateras per rätt
                                     bg=BAKGRUNDSFÄRG,  # Bakgrundsfärgen för labeln.
                                     font=('Consolas', 14),  # Typsnittet för texten
                                     relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                     bd=5)  # Boardens storlek
        # Labeln ska visa antalet fel matchningar som spelaren gör, texten kommer alltså att uppdateras för varje runda
        self.antal_fel_text = Label(self.frame_label_knapp,  # Fönstret där labeln visas
                                    text="Antal Fel: " + str(self.antal_fel),  # Texten på labeln, uppdateras per fel
                                    bg=BAKGRUNDSFÄRG,  # Bakgrundsfärgen för labeln.
                                    font=('Consolas', 14),  # Typsnittet för texten
                                    relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                    bd=5)  # Boardens storlek

        # Knappen ska spara resultatet i en highscorelista
        self.spara_ny_fil_knapp = Button(self.frame_label_knapp,  # Fönstret där knappen visas
                                         text="SPARA RESULTAT",  # Texten på knappen
                                         state='disabled',  # Knappen är avaktiverad
                                         font=('Consolas', 14),  # Typsnittet för texten
                                         bg=KNAPPFÄRG,  # Färgen för knappen
                                         activebackground=KNAPPFÄRG,  # Färgen för knappen ändras ej vid tryck
                                         fg='Black',  # Färgen för texten
                                         activeforeground='Black',  # Färgen på texten ändras ej
                                         # Anropar på metoden spara_resultat_i_fil vid knapp tryck
                                         command=self.spara_resultat_i_fil)

        # OBS, dessa labels placeras strikt under varandra, pga ingen modifiering av placering
        self.match_eller_ej.pack(side=RIGHT, padx=30)  # Lägger till labeln i fönstret
        self.antal_rätt_text.pack(side=RIGHT, padx=5)  # Lägger till labeln i fönstret
        self.antal_fel_text.pack(side=RIGHT, padx=15)  # Lägger till labeln i fönstret

        self.spara_ny_fil_knapp.pack(side=LEFT, padx=10)  # Lägger till knappen i fönstret

        for i in range(0, self.antal_rader * self.antal_kolumner):
            siffra = str(i)  # Används för att urskilja vilken spel-knapp son trycks
            knapp_namn = "b" + siffra  # Variabeln kommer användas för att döpa varje spel-knapp i matrisen
            self.knapp_namn.append(knapp_namn)  # Variabeln läggs in i listan "knapp_namn"
            self.knapp_objekt_lista.append(knapp_namn)  # Variabeln läggs in i listan "knapp_objekt_lista"

            # Skapar knappar för motsvarande knappnamn
            self.knapp_objekt_lista[i] = Button(self.frame,  # Framen i fönstret där spel-knappen ska visas
                                                text=' ',  # Texten är till en början tom
                                                font=('Arial', 10),  # Typsnittet för texten
                                                height=2,  # Höjden för knappen
                                                width=8,  # Bredden för knappen
                                                fg="black",  # Textens färg är svart
                                                # När man trycker kommer färgen på texten fortfarande vara svart
                                                activeforeground="black",
                                                bg="white",  # Knappens färg är vit
                                                # Knappens färg är fortfarande vit under tiden som man trycker
                                                activebackground="white",
                                                # lamda funktionen accepterar några argument
                                                # "knapp_tryck" funktionen tar in argumenten till dess parametrar
                                                command=lambda
                                                    knapp=self.knapp_objekt_lista[i],  # Vilken spel-knapp det är sparas
                                                    listsiffra=i:  # Siffran avgör vilket ord spel-knappen motsvarar
                                                # Metoden "knapp_tryck()" anropas vid knapptryck
                                                self.knapp_tryck(knapp, listsiffra))

        print(self.knapp_objekt_lista)

        self.öppna_fil_ord()  # Metoden "öpna_fil_ord" anropas
        self.justerar_knapp_position()  # Metoden "placera_knapp" anropas

    def öppna_fil_ord(self):
        """
        Öppnar filen "vanliga.txt", läser igenom filen radvis med en for-loop, varje ord från filen lagras i listan
        "ord_lista", listan kommer att slumpas för att sedan igen gå igenom en for-loop för att rensa
        listan och ha A antal ord. Dessa ord är ord som spelaren ska försöka matcha med varandra,
        A baseras på matrisensstorlek, ex om användaren vill spela i ett 6x6 format så
        kommer A:et i detta fall vara 18, eftersom antalet knappar totalt är 36. Därmed är det 18 ord kvar i listan.
        Sedan adderas dessa 18 ord igen i listan med en for-loop. Detta ger oss två av varje ord.
        """
        with open("vanliga.txt", 'r', encoding='utf-8') as fil:
            """Funktionen "open" öppnar filen med namnet "vanliga.txt" för läsning och registrering i en lista"""
            for rad in fil:  # Med hjälp av en for-loop går vi igenom filen rad för rad som läggs till i listan
                rad = rad.strip()  # Tar bort extra radbrytningar i den stäng som läses in
                self.ord_lista.append(rad)  # Sparar alla ord i listan "ord_lista"

        random.shuffle(self.ord_lista)  # Slumpar alla ord i listan "ord_lista"

        """Loopen syfte är att rensa listan och ha A antal ord, där dessa ord ska vara de ord som man ska försöka 
        matcha med varandra"""
        for i in range(len(self.ord_lista), self.antal_rader * (self.antal_rader // 2), -1):
            self.ord_lista.pop()  # Raderar ett element vilket är ett ord, denna process pågår baklänges,
            # tills listan har A antal ord kvar

        # Duplicerar alla ord som redan finns i listan. Får två av samma ord i listan
        for i in range(len(self.ord_lista)):
            element_från_lista = self.ord_lista[i]  # Tillfällig variabel som används för att duplicera orden i listan
            self.ord_lista.append(element_från_lista)  # Lägger till samma ord i listan igen

        random.shuffle(self.ord_lista)  # Slumpar listan
        print(self.ord_lista)

    def justerar_knapp_position(self):
        """
        Placerar spel-knapparna kolumn och radvis
        """
        antal_koloner = int(self.antal_kolumner)  # Antalet koloner i matrisen
        antal_rader = int(self.antal_rader)  # Antalet rader i matrisen

        knapp_element = 0
        # Placerar alla knappar kolon- och radvist
        for koloner in range(0, antal_koloner):
            for rader in range(0, antal_rader):
                knapp = self.knapp_objekt_lista[knapp_element]
                knapp.grid(row=rader, column=koloner)
                knapp_element += 1

    def knapp_tryck(self, specifik_knapp, siffra):
        """
        Metoden som alla spel-knappar anropar på när användaren trycker på en spel-knapp. Metod visar det gömda
        ordet samt sparar den valda knapptrycket i listan "valda_knappar", på så sätt kan vi senare jämföra
        de specifika orden till de specifika knapparna och se om orden är lika eller inte, "antal_valda_knappar"
        ökar även med 1
        """

        # Loopar igenom hela knapp_namn listan för att finna det knappnamn som är detsamma som parametern specifik_knapp
        for i in range(len(self.knapp_namn)):
            if specifik_knapp == self.knapp_namn[i] and self.antal_valda_knappar < 2:
                # Ändrar texten för knappen till ordet den knappen motsvarar
                self.knapp_objekt_lista[i].config(text=self.ord_lista[siffra],  # Texten blir ordet
                                                  state='disabled')  # Avaktiverar knappen, kan ej trycka på den igen

                # Håller koll på vilken knapp som trycktes, listan används senare för att jämföra orden med varandra
                self.valda_knappar_lista.append(siffra)
                # antal_valda_knappar ökas med ett, detta för att hålla koll på hur många knappar som väljs.
                self.antal_valda_knappar += 1
                print(self.valda_knappar_lista)
            # Om antalet_valda_knappar är detsamma som 2 har användaren valt två styckna knappar att jämföra.
            if self.antal_valda_knappar == 2:
                self.jämför_svar()  # Anropar metoden "jämför_svar()"

    def jämför_svar(self):
        """
        Om "antal_valda_knappar" = 2 har användaren valt två knappar i denna metod ska dessa knappars gömda
        ord jämföras, detta görs då genom att jämföra siffrorna lagrade i "valda_knappar_lista" eftersom siffrorna
        motsvarar de ord i "ord_lista" Om det visar sig att det blev en matchning nollställs
        "antal_valda_knappar", "valda_knappar_lista" eftersom dessa ska vara tom så att vi kan jämföra de
        tva andra knapparna som användaren väljer att välja nästa försök, här ökas även "antal_rätt" med 1. Dessutom
        kommer knapparna att bli avaktiverade så att användaren inte kan trycka på dessa knappar igen då den redan
        hittat dess matchningar. Om det inte blev en matchning så kommer vi fortfarande nollställa
        "antal_valda_knappar", "valda_knappar_lista" så vill vi att ordet på knappen ska "gömmas". Nu kommer istället
        "antal_fel" att ökas med 1
        """

        # Jämför om orden är detsamma
        if self.ord_lista[self.valda_knappar_lista[0]] == self.ord_lista[self.valda_knappar_lista[1]]:

            # Går igenom hela "valda_knappar_lista"
            for i in range(len(self.valda_knappar_lista)):
                print(self.valda_knappar_lista)
                self.rätt_svar.append(self.valda_knappar_lista[i])  # Lägger till alla rätta matchningar i listan
            self.avaktivera_rätt_knapp(self.rätt_svar)  # Avaktiverar rätt knapp matchning

            self.antal_rätt += 1  # "antal_rätt" ökas med 1
            # antal_rätt_text uppdateras
            self.antal_rätt_text.config(text="Antal Rätt " + str(self.antal_rätt))
            # "match_eller_ej" uppdateras
            self.match_eller_ej.config(text="RÄTT!!!",  # Texten som visas i labeln
                                       bg='lime green',  # Bakgrundsfärgen ändras till lime grönt
                                       relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                       bd=5)  # Boarderns storlek
            self.antal_valda_knappar = 0  # Klassatributen nollställs
            self.valda_knappar_lista.clear()  # Listan nollställs
        # Om det visar sig att orden inte är detsamma
        else:
            # "match_eller_ej" uppdateras
            self.match_eller_ej.config(text="FEL!!!",  # Texten som visas i labeln
                                       bg='firebrick2',  # Bakgrundsfärgen ändras till rött
                                       relief=RAISED,  # Skapar en boarder av typen "RAISED"
                                       bd=5)  # Boarderns storlek
            self.antal_fel += 1  # "antal_fel" ökas med 1
            # antal_fel_text uppdateras
            self.antal_fel_text.config(text="Antal Fel " + str(self.antal_fel))

            # De valda knapparnas färg ändras till rött
            for element in range(len(self.valda_knappar_lista)):
                self.knapp_objekt_lista[self.valda_knappar_lista[element]].config(bg="firebrick2")

            self.avaktivera_alla_knappar()  # Avaktiverar alla knappar
            meddelande.showinfo("Fel Matchning", "Fel matchning testa igen")
            self.aktivera_knappar()  # Aktiverar alla knappar
            self.avaktivera_rätt_knapp(self.rätt_svar)  # Avaktiverar rätt knapp matchning

            # Ändrar tillbaka färgen på knappen till vitt och gömmer orden
            for element in range(len(self.valda_knappar_lista)):
                self.knapp_objekt_lista[self.valda_knappar_lista[element]].config(text=" ",  # Gömmer orden
                                                                                  bg="white")  # Knapp färgen blir vit
            self.antal_valda_knappar = 0  # Nollställer antalet_valda_knappar
            self.valda_knappar_lista.clear()  # Nollställer listan

        # Om spelaren hittat alla matchningar ska resultatet sparas
        if self.antal_rätt == self.antal_rader * (self.antal_rader // 2):
            self.spara_ny_fil_knapp.config(state='normal',  # Knappen går att trycka
                                           bg='lime green',  # Ändrar knappfärgen till lime grönt
                                           activebackground='lime green')  # Färgen ändras vid klick av knappen

    def avaktivera_rätt_knapp(self, rätt_svar):
        """
        Avaktiverar alla de matchade knapparna och gör deras färger till grönt
        """
        # Går igenom alla rätta matchningar och avaktiverar de samt ändrar dess färg
        for rätt_knapp in range(len(rätt_svar)):
            self.knapp_objekt_lista[rätt_svar[rätt_knapp]].config(state='disabled',  # Avaktiverar knappen
                                                                  bg='lime green')  # Knappfärg blir lime grönt

    def aktivera_knappar(self):
        """
        Aktiverar alla knappar
        """
        # Går igenom alla knappar och aktiverar de
        for knapp in range(self.antal_rader * self.antal_kolumner):
            self.knapp_objekt_lista[knapp].config(state='active')

    def avaktivera_alla_knappar(self):
        """
        Avaktiverar alla knappar, detta för att användaren inte ska kunna klicka på andra knappar när den haft fel.
        """
        # Går igenom alla knappar och avaktiverar de
        for knapp in range(self.antal_rader * self.antal_kolumner):
            self.knapp_objekt_lista[knapp].config(state='disabled')

    def spara_resultat_i_fil(self):
        self.spara_ny_fil_knapp.config(state='disabled')
        matrisstorlek_text = str(self.antal_rader) + "X" + str(self.antal_kolumner)
        highscore_lista_filnamn = 'HIGHSCORE_' + matrisstorlek_text + '.txt'
        SparaResultat(highscore_lista_filnamn, self.spelar_namn, self.antal_fel)


class SparaResultat:
    """
    Klassen sparar spelarens resultat på en sorterad highscorelista i en fil.
    """

    def __init__(self, highscore_lista_filnamn, spelar_namn, antal_fel):
        self.spelar_namn = spelar_namn
        self.antal_fel = antal_fel
        # Attributen används för att öppna/skapa en highscore fil beroende på matrisens storlek
        self.highscore_lista_filnamn = highscore_lista_filnamn
        self.spelarnamn_och_antal_fel = []  # Lista som både sparar spelarens namn samt dess antala felgissningar
        self.lista_spelarnamn = []  # Lista som sparar tidigare spelarnas namn
        self.lista_antal_fel = []  # Lista som sparar antalet fel matchningar i ordning
        self.lista_spelar_position = []  # Lista som sparar tidigare spelare samt den senaste spelarens rank i ordning
        self.uppdaterad_lista_spelarnamn = []  # Lista som sparar alla spelarnas namn i rätt ordning
        self.nuvarande_position_spelare = 0  # Används vid positionering av den senaste spelaren i highscorelistan
        # Om den senaste spelaren fått flest antal fel jämfört med tidigare spelare ska den vara "True"
        self.sämst_resultat = True

        self.öppna_fil_highscore()

    def öppna_fil_highscore(self):
        """
        Metoden sparar alla rader från en tillgänglig higscorelista i listan "spelarnamn_och_antal_fel". Anropar
        sedan metoden slicing_rader. Om det visar sig att en sådan highscorelista för den specifika matrisen inte
        finns skapas en ny highscore fil för den matristen
        """
        try:  # Om det finns en tidigare highscore fil för matrisen
            highscore_lista = open(self.highscore_lista_filnamn, 'r')
            """Funktionen "open" öppnar filen med namnet användarens_fil_inmatning för läsning"""
            for line in highscore_lista:  # Med hjälp av en for-loop går vi igenom filen rad för rad som läggs till i listan
                line = line.strip()  # Tar bort extra radbrytningar i den stäng som läses in
                self.spelarnamn_och_antal_fel.append(line)  # Raden läggs till i listan som ett element
            highscore_lista.close()  # Stänger filen
            # Anropar på metoden "slicing_rader"
            self.slicing_rader()
            # Returnerar fönster och namnet på fönstret till highscore fönstret
            ny_fönster, fönster_namn = skapa_nya_fönster(FÖNSTERTYP[4])
            # Anropar klassen "HighscoreFönster"
            HighscoreFönster(self.highscore_lista_filnamn, ny_fönster, fönster_namn)

        except FileNotFoundError:  # Om det inte finns en tidigare highscore fil för matrisen
            print(self.highscore_lista_filnamn)
            print("ja")
            highscore_lista = open(self.highscore_lista_filnamn, 'x')  # Skapar en ny fil
            highscore_lista.write("1. Spelarnamn: " + str(self.spelar_namn) + "\n" +
                                  "Antal Fel: " + str(self.antal_fel))
            highscore_lista.close()  # Stänger filen
            # Returnerar fönster och namnet på fönstret till highscore fönstret
            ny_fönster, fönster_namn = skapa_nya_fönster(FÖNSTERTYP[4])
            # Anropar klassen "HighscoreFönster"
            HighscoreFönster(self.highscore_lista_filnamn, ny_fönster, fönster_namn)

    def slicing_rader(self):
        """
        Metoden Sclicar raderna så att enbart spelarnamn, antal fel samt ranking sparas och lagras i variablerna
        "spelarnamn", "spelar_position" respektiv "antal_fel_siffror". Dessa variabler lagras sedan i respektiv
        lista: "lista_spelarnamn", "lista_spelar_position", "lista_antal_fel". Metoden anropar sedan på
        """
        for spelarnamn in range(0, len(self.spelarnamn_och_antal_fel), 2):
            """For-loopen går igenom varje rad som har med spelarnas namn att göra. Enbart spelarnas plats samt namn 
            kommer att lagras i vardera lista.
            """
            namn = self.spelarnamn_och_antal_fel[spelarnamn]  # Lagrar hela raden i variabeln namn
            punkt = namn.find(".")  # Lagrar vilket index som en punkt ligger i raden.
            spelar_position = int(namn[0:punkt])  # Sparar endast placeringsnumret i variabeln
            kolon = namn.find(":")  # Lagrar vilket index som ett kolon ligger i raden.
            spelarnamn = namn[kolon + 2:]  # Kolonet & mellanrummet innan namnet ska inte tas med

            self.lista_spelarnamn.append(spelarnamn)  # Lägger till variabeln "spelarnamn" i listan
            self.lista_spelar_position.append(spelar_position)  # Lägger till variabeln "spelar_position" i listan

        # For-loopen går igenom varje rad som har med de tidigare spelarnas antal fel att göra.
        for antal_fel in range(1, len(self.spelarnamn_och_antal_fel), 2):
            antal_fel_text = self.spelarnamn_och_antal_fel[antal_fel]  # Lagrar hela raden i variabeln "antal_fel_text"
            kolon_fel = antal_fel_text.find(":")  # Lagrar vilket index som ett kolon ligger i raden
            antal_fel_siffror = int(antal_fel_text[kolon_fel + 2:])  # Kolonet & mellanrummet innan namnet tas inte med
            self.lista_antal_fel.append(antal_fel_siffror)  # Lägger till variabeln "antal_fel_siffror" i listan

        self.hur_ska_sorteringen_gå_till()

    def hur_ska_sorteringen_gå_till(self):
        """
        Sorteringen baseras utifrån spelarens resultat. Beroende på resultat kommer sorteringen att sortera på olika
        sätt
        """
        # For-loopen anpassar listan "lista_spelar_position" utifrån den senaste spelarens resultat
        for i in range(len(self.lista_antal_fel)):
            if self.antal_fel < self.lista_antal_fel[i]:
                """Om spelaren fått mindre antal fel än andra spelare som spelat spelet på samma matris kommer 
                placeringsnumret för dessa tidigare spelare ökas med 1 då de placeras ett steg under spelaren som 
                fick bättre resultat"""
                nuvarande_position = self.lista_spelar_position[i]
                self.lista_spelar_position[i] = nuvarande_position + 1
                self.sämst_resultat = False

            elif self.antal_fel == self.lista_antal_fel[i]:

                """Om spelaren fått samma resultat som en annan spelare kommer loopen att avbrytas och 
                placeringsnummret som den tidigare spelaren hade kommer att sparas och lagras i variabeln 
                "nuvarande_position_spelare" """
                self.nuvarande_position_spelare = self.lista_spelar_position[i]
                self.sämst_resultat = False
                break
        # Anropar på metoden "sortering_av_spelare"
        self.sortering_av_spelare()

    def sortering_av_spelare(self):
        """
        Metoden sorterar spelarens resultat utfirån resultatet från metoden "hur_ska_sorteringen_gå_till"
        """
        # Om spelaren har ett resultat som är detsamma som någon annan spelare och inte fått sämst resultat, körs if-satsen
        if self.nuvarande_position_spelare != 0 and self.sämst_resultat == False:
            print("Först if-hära")
            # Den senaste spelarens plats läggs till i listan
            self.lista_spelar_position.append(self.nuvarande_position_spelare)
            # Sorterar listan från minsta till högsta värdet, detta motsvarar högsta placeringen till lägsta placeringen
            self.lista_spelar_position.sort()
            # Anropar metoden "sortera_spelarnamn"
            self.sortera_spelarnamn()
        else:
            """
            Om spelaren inte har ett resultat som är detsamma som någon annan spelare samt kanske har sämsta 
            resultaten kommer denna else-sats att köras för att avgöra ifall spelaren fått sämst resultat eller inte 
            och utifrån denna slutsats sortera samt registrera spelaren. 
            """
            print("else")
            # Om spelaren inte fått sämst resultat kommer denna if-sats att köras
            if not self.sämst_resultat:
                print("Första if")
                print(self.lista_spelar_position)
                # Tar reda på vilken det lägsta placeringen är och sparar den i en variabel
                sista_plats_högsta = max(self.lista_spelar_position) + 1
                print(sista_plats_högsta)
                print(self.lista_spelar_position)

                for plats_saknas in range(1, sista_plats_högsta):
                    """
                    Eftersom placeringen för den senaste spelaren saknas kommer en for-loop att köras för att ta 
                    reda på vilket nummer som saknas i listan "lista_spelar_position". Den saknade numret är detsamma 
                    som den senaste spelarens placering i highscorelistan. 
                    """
                    if plats_saknas in self.lista_spelar_position:
                        pass  # Om "platsen" redan finns är det inte ranken för den senaste spelaren.
                    else:
                        self.nuvarande_position_spelare = plats_saknas  # Lägger till den saknade placeringen i variabeln
                        self.lista_spelar_position.append(
                            self.nuvarande_position_spelare)  # Lägger till den saknade placeringen i listan
                        # Lista sorteras från minsta till högsta värdet, vilket motsvarar högsta placeringen till lägsta placeringen
                        self.lista_spelar_position.sort()

            # Om spelaren fått sämst resultat kommer denna else-sats att köras
            else:
                print("else- andra")
                self.nuvarande_position_spelare = max(
                    self.lista_spelar_position) + 1  # Spelarens rank är den sista platsen
                self.lista_spelar_position.append(
                    self.nuvarande_position_spelare)  # Lägger till spelarens plats i listan
                # Lista sorteras från minsta till högsta värdet, vilket motsvarar högsta placeringen till lägsta placeringen
                self.lista_spelar_position.sort()
            # Anropar metoden "sortera_spelarnamn()"
            self.sortera_spelarnamn()
        # Anropar metoden "slutför_registrering"
        self.slutför_registrering()

    def sortera_spelarnamn(self):
        """
        For-loopen sorterar samt lägger till de gamla samt den senaste spelaren i en ny lista. Eftersom loopen
        loopar fler antal gånger än vad det finns antal element i listan "lista_spelarnamn" kommer loopen avbrytas
        efter att den senaste spelarens placering har hittats och läggs till i listan i samma index som spelarens
        placerings index samt antal fel index. På detta sätt motsvarar varje samma index för ett element i listorna
        samma spelare.
        """
        self.lista_antal_fel.append(self.antal_fel)  # Den senaste spelarens antal fel läggs till i listan
        self.lista_antal_fel.sort()  # Sorterar listan från minsta till högsta antal fel
        start = 0  # Variabeln kommer användas för
        for i in range(len(self.lista_spelar_position)):
            # När listan har samma index som den nuvarande spelarens placering körs if-satsen
            if i == self.lista_spelar_position.index(self.nuvarande_position_spelare):
                # Lägger till spelarens namn i den uppdaterade listan
                self.uppdaterad_lista_spelarnamn.append(self.spelar_namn)
                # Variabeln används för nästa for-loop för att registrera namn som är kvar i den uppdaterade namn listan
                start = i
                break
            else:
                self.uppdaterad_lista_spelarnamn.append(self.lista_spelarnamn[i])

        # Om spelaren fick bäst resultat körs denna if-sats
        if not self.sämst_resultat:
            print("Ja det är den")
            # Loopen börjar på där den slutade och lägger till de resterade namnet i "uppdaterad_lista_spelarnamn"
            print(start)
            for resten in range(start, len(self.lista_spelarnamn)):
                self.uppdaterad_lista_spelarnamn.append(self.lista_spelarnamn[resten])
                print(self.lista_spelarnamn[resten])

    def slutför_registrering(self):
        """
        Skriver in den nya highscoren i samma fil
        """
        # Öppnar highscorefilen för skrivning, obs texten innan raderas.
        highscore_lista = open(self.highscore_lista_filnamn, 'w')
        # For-loopen lägger till spelarnas resultat i en highscorelista.
        for i in range(len(self.uppdaterad_lista_spelarnamn)):
            highscore_lista.write(str(self.lista_spelar_position[i]) + ". Spelarnamn: " + str(
                self.uppdaterad_lista_spelarnamn[i]) + "\n" + "Antal Fel: " + str(self.lista_antal_fel[i]) + "\n")
        highscore_lista.close()  # Stänger filen


class HighscoreFönster(FönsterEgenskaper):
    """
    Klassen presenterar highscore-listan på ett nytt fönster.
    """

    def __init__(self, highscore_lista_filnamn, fönster, titel):
        super().__init__(fönster, titel)  # Klassen får tillgång till "FönsterEgenskaper" attribut samt klass metoder
        self.label_rubrik = Label(fönster,  # Fönstret där labeln visas
                                  text=titel,  # Texten för rubriken
                                  font=('Arial', 50, 'bold'),  # Typsnittet för rubriken
                                  bg=BAKGRUNDSFÄRG,  # Bakgrundsfärgen för rubriken
                                  fg='firebrick3',
                                  bd=5,  # Boarderns storlek
                                  relief=RIDGE)  # Vilken typ av boarder
        self.label_rubrik.pack(pady=20)
        self.highscore_text = Text(fönster,
                                   width=40,  # Bredden för boardern bh
                                   height=30,  # Höjden för boardern
                                   font=('Arial', 14, 'bold'),
                                   bd=10,  # Boarderns storlek
                                   relief=GROOVE)  # Vilken typ av boarder
        self.highscore_text.pack(pady=30)
        self.rader_lista = []
        self.highscore_lista_filnamn = highscore_lista_filnamn
        self.ny_fönster_highscore()

        FönsterEgenskaper.avsluta(self)  # Anropar på en klass metod som ska felhantera avslutning av ett fönster

    def ny_fönster_highscore(self):
        """
        Metoden öppnar highscore-listan för den specifika matrisen spelaren spelade på och lägger in varje rad i en
        textbox med hjälp av en lista
        """
        with open(self.highscore_lista_filnamn, 'r') as highscore_lista:
            """Funktionen "open" öppnar filen med namnet "vanliga.txt" för läsning och registrering i en lista"""
            for line in highscore_lista:  # for-loopen går igenom filen rad för rad som läggs till i listan
                line = line.strip()  # Tar bort extra radbrytningar i den stäng som läses in
                print(line)
                self.rader_lista.append(line)  # Lägger till filens rader i listan
        print(self.rader_lista)

        for rank in range(len(self.rader_lista)):
            self.highscore_text.insert(END,  # "END, syftar på den sista tecknet på den föregående meningen"
                                       # Lägger till varje rad från filen som är lagrad i listan i textrutan.
                                       self.rader_lista[rank] + "\n")
        self.highscore_text.config(state='disabled')  # Avaktiverar textrutan, spelaren kan ej redigera texten


def memory_main():
    """
    Huvudkod för hela programmet, här börjar och slutar programmet.
    """
    startsida_fönster = Tk()  # Skapar ett fönster, specifikt ska detta fönster vara startsidans fönster
    StartsidaFönster(startsida_fönster, FÖNSTERTYP[0])  # Klassen anropas och tar med två variabler som parametrar

    startsida_fönster.mainloop()  # Placerar fönstret på datorskärmen och avaktar på vidare händelser


memory_main()
