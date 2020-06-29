import kivy
from kivy.app import App
import shapefile
import geopandas as gpd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from shapely.geometry import shape
from shapely.geometry import *
from shapely.geometry.polygon import *
import sys
class python_proj(App):
   def build(self):
        

        num=int()
        gpandas=[] #to store data from shapefile read by geopandas
        data=[] # to store all the datas of all shapefiles
        data_each=[] 
        files=[]
        button=[]
        checkout_vars = []
        file_names=[]
        #creating main Window
        root=Tk()
        root.title("Geospatial Mining")
        root.geometry("+500+500")
        var=IntVar()
        set_checked = set()
        Label(root,text="enter no. of shapefiles-->",bg="black",fg="white",relief=RIDGE, width=20).grid(row=0,column=0)
        text_area=Text(root,width=2,height=1)
        text_area.grid(row=0,column=1)


        def fileopen():
            #global num
            global checkout_vars
            num = int(text_area.get("1.0", 'end-1c'))
            for x in range(num):
                checkout_vars.append(IntVar())

            print("I got = ", num)
            for i in range(num):
                data.append([])
                files.append(i)
                gpandas.append(i)
                file_names.append(i)
                file = askopenfilename(defaultextension=".shp", filetypes=[("All Files","*.*")])
                if file == "": 
                    print("INVALID FILENAME")
                    # no file to open 
                    file = None
                else: 
                    
                    gpandas[i]=gpd.read_file(file)
                    files[i] = (shapefile.Reader(file))
                    print (files[i])
                    for j in range(len(files[i])):
                        data_each.append(j)
                        data_each[j]=shape(files[i].shapeRecords()[j].shape.__geo_interface__)
                        data[i].append(data_each[j])

                print (len(data[i]))
                file_names[i]=os.path.basename(file)
                button.append(i)
                button[i]=Checkbutton(root,text=file_names[i],variable=checkout_vars[i],onvalue = 1, offvalue = 0).grid(row=2+i)


        opn=Button(root,text="open",command=fileopen,relief=GROOVE,fg="green").grid(row=0,column=2)



        def showCoordinates():#displaying coordinates
             
            selected = [ ind for ind,var_val in enumerate(checkout_vars) if var_val.get() == 1]
            print ("Coordinates of file"+str(selected)+"\n\n")
            for i in selected:
                for j in range(len(data[i])):
                    print ("Coordinates of "+file_names[i]+"::")
                    print (data[i][j])
                    print("\n\n\n")
            
        coord=Button(root,text="Coordinates",command=showCoordinates,activebackground="green").grid(row=3,column=10, sticky = W, pady = 2)

        def showshape():#displaying shapefiles
            
            num = int(text_area.get("1.0", 'end-1c'))

            for i in range(num):
                gpandas[i].plot(color='green', edgecolor='black')
                plt.title('Shape of'+file_names[i]) 
            plt.show() 
            

        shpe=Button(root,text="Your_Shp",command=showshape,activebackground="green").grid(row=5,column=10)

        def uniongis():#displaying union

            selected = [ ind for ind,var_val in enumerate(checkout_vars) if var_val.get() == 1]

            for i in selected:
                           
                print (i)
                
               #checking geom_type of 1st data
                if data[i][0].geom_type == "Polygon":
                    first = data[i][0]
                    for x in range( len(data[i])):
                        first = first.union(data[i][x])


                    x,y = first.exterior.xy
                    plt.plot(x,y,color="green")

               #checking geom_type of 1st data
                elif data[i][0].geom_type == "LineString" or data[i][0].geom_type == "MultiLineString":
                    for ind in range(0, len(data[i])):

                        #handling assertion error
                        assert(data[i][ind].geom_type == "LineString" or data[i][ind].geom_type == "MultiLineString" )

                        if data[i][ind].type == "LineString":
                            x,y=data[i][ind].xy
                            plt.plot(x,y,color="blue")

                        if data[i][ind].type == "MultiLineString":
                            for line_string in data[i][ind]:
                                x,y = line_string.xy
                                plt.plot(x,y,color="blue")
                
                        
            plt.title('Union')       
            plt.show()
            


        unn=Button(root,text="Union",command=uniongis,activebackground="green").grid(row=7,column=10)
        def intersectiongis():#displaying intersection
            interlist=[]
            selected = [ ind for ind,var_val in enumerate(checkout_vars) if var_val.get() == 1]

         

            for i in selected:
                
                print (i)
                interlist.append(i)
                for j in range(len(data[i])):
                    try:#handling index error
                        if (len(data[i])>1):
                            final=data[i][j].intersection(data[i][j+1])
                            print (final.geom_type)
                            
                            if (final.geom_type=="GeometryCollection"):

                                for xx in final:

                                    x,y = xx.exterior.xy
                                    plt.plot(x,y,color="purple")
                            if (final.geom_type=="MultiLineString"):
                                for xx in final:
                                    x,y = xx.xy
                                    plt.plot(x,y,color="blue")


                            if (final.geom_type=="Point"):
                                x,y=final.xy
                                plt.plot(x,y,color="black")
                            else:

                                for xx in final:
                                    x,y = xx.xy
                                    plt.plot(x,y,color="pink")
                        elif (len(data[i])==1 ):
                                final=data[i][0].intersection(data[i+1][0])
                                print (final.geom_type) 
                                for xx in final:
                                    x,y=xx.xy
                                    plt.plot(x,y,color="red")
                    except IndexError as e:
                        pass
            plt.title('Intersection')         
            plt.show()
        intrsction=Button(root,text="Intersection",command=intersectiongis,activebackground="green").grid(row=9,column=10)

        def buffergis():
            selected = [ ind for ind,var_val in enumerate(checkout_vars) if var_val.get() == 1]
            for i in selected:

                gpandas[i].plot(color='yellow', edgecolor='black')
               
                d=float(input("enter buffer value: "))
                for j in range(len(data[i])):
                    c1=data[i][j].buffer(d)
                    print (c1.geom_type)
                    if (c1.geom_type=="Polygon"):

                        x1,y1 = c1.exterior.xy
                        plt.plot(x1,y1,color="green")
                    elif (c1.geom_type=="MultiPolygon"):
                        for mulpol in c1:
                            x2,y2=mulpol.exterior.xy
                            plt.plot(x2,y2,color="green")

            plt.title("Buffer")
            plt.show()

        buffers=Button(root,text="Buffer of each",command=buffergis,activebackground="green").grid(row=11,column=10)

        def chckbuffer():
            selected = [ ind for ind,var_val in enumerate(checkout_vars) if var_val.get() == 1]
            for i in selected:
                

                buf_value=float(input("enter buffer value: "))
                for j in range(len(data[i])):
                    c1=data[i][j].buffer(buf_value)
                    print (c1.geom_type)
                    if (c1.geom_type=="Polygon"):

                        x1,y1 = c1.exterior.xy
                        plt.plot(x1,y1,color="green")
                    elif (c1.geom_type=="MultiPolygon"):
                        for mulpol in c1:
                            x2,y2=mulpol.exterior.xy
                            plt.plot(x2,y2,color="green")

            plt.title("Buffer")
            plt.show()

        chck1=Button(root,text="Buffer of all",command=chckbuffer,activebackground="green").grid(row=13,column=10)


        root.mainloop()
if __name__=="__main__":
	python_proj().run()
