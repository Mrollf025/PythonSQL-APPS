import pandas as pd
import psycopg2 as ps

# simple script that takes in a csv files, and checks the publisher and developer
# column against my PostgreSQL Games DB/company table, and gives a list of missing
# companies

# Step 1 ingest csv into a pandas data frame

# Step 2 query games/company table, store the data

# Step 3 check the publisher and developer columns from the CSV against
# the company table. If a company does not have a direct match place that 
# company into a list.

# Step 4 take the new list and insert those companies into the table
# now we query the Genre table,The region Table, and the company table
# then match these columns to column ID's and change the value of the match
# to the column value


#Step 5 now with the modified column data we can insert all the games into
#the Games/games table

##Pandas code here##
##create data frame
csv_df= pd.read_csv('PY-SQL/PythonSQL-APPS/50-GB-Games-List.csv',index_col=False)
csv_publisher_names = csv_df['Publisher']
csv_developer_names = csv_df['Developer']

#lets compare these two lists
unique_to_publishers = list(set(csv_publisher_names)- set(csv_developer_names))
unique_to_developers = list(set(csv_developer_names)- set(unique_to_publishers))

#combine these into one list
all_unique_companies = unique_to_developers+unique_to_publishers

#print(all_unique_companies)
## psycopg2 connection/ SQL code here ##
class SQL:
    def __init__(self):
        pass

    def connect(self):
        return ps.connect(
            dbname="GAMES",
            user="postgres",
            password="7354",
            host="localhost",
            port="5432"
        )
    
    def list_company(self):
        try:
            conn = self.connect()
            cur= conn.cursor()
            cur.execute("""
                SELECT 
                        * 
                FROM 
                        company 
                ORDER BY 
                        company_name ASC
                    """)
            ### fetch results
            results = cur.fetchall()
            
            #convert to data frame
            companies_df = pd.DataFrame(results,columns=['company_id','company_name','region_id'])
            return companies_df
            
        except Exception as e:
            print("Error:",e)
            return pd.DataFrame()
        finally:
            cur.close()  # Close the cursor
            conn.close()
    
    def list_region(self):
        try:
            conn = self.connect()
            cur= conn.cursor()
            cur.execute("""
                SELECT 
                        * 
                FROM 
                        region 
                ORDER BY 
                        region_ID ASC
                    """)
            ### fetch results
            results = cur.fetchall()
            
            #convert to data frame
            region_df = pd.DataFrame(results,columns=['region_id','region_name','region_abbriviation'])
            return region_df
            
        except Exception as e:
            print("Error:",e)
            return pd.DataFrame()
        finally:
            cur.close()  # Close the cursor
            conn.close()

## compare data frame values here ##
## we need to instatiate the sql class
app = SQL()




def compare_comp_dataframes():
    #get the sql data and turn into a list
    comp_dataframe = app.list_company()
    comp_names = comp_dataframe['company_name'].tolist()
    

    csv_list = all_unique_companies

    unique_values = list(set(csv_list)- set(comp_names))
    return unique_values
        
if __name__ == "__main__":
    print(app.list_company())
    print(compare_comp_dataframes())

