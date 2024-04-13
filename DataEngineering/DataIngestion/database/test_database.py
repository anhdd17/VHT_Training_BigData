from database import MyPostgreSQL

if __name__ == '__main__':
    mydb = MyPostgreSQL(database='datalake', user='airflow', password='airflow', 
                        host='192.168.1.205', port=5433)

    # check if exist si_id = 1 in database
    print(mydb.check_exists(table='event', condition=f"si_id = 'si_A'"))

    # string1 = "[\"Asian\", \"Female\", \"20-29\"]"
    # string2 = "[\"di\", \"di\", \"di\", \"di\", \"li\"]"
    # res = mydb.insert(
    #     table = "event",
    #     column = ("si_id", "group_id", "user_id", "source_id", "object_id", "bbox", 
    #               "confidence", "image_path", "time_stamp", "fair_face", "person_id", "dict"),
    #     values = ("si_A", "group_A", "trongdat", "test", "123", "[1077, 180, 1323, 513]", 
    #               0.8105192184448242, "http://minio:9000/vss/s3%3A//vss/face/1682048755_test_0.jpg?AWSAccessKeyId=admin&Signature=Vo3i6U%2FCbSxoR6KzCJWf2VMRMSI%3D&Expires=1683609146", 
    #               "1683605546171", string1, string2, "[0.8942996263504028, 0.9111446738243103, 0.9411799907684326, 0.9483562707901001, 0.9508835077285767]")
    # )
    # print("Status insert: ", res)
    mydb.close()
    
    