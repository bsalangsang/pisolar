import sqlExec
import datetime

################Variables######################
sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()
###############################################


class modFunc:
    def __init__(self, dbCon):
       self.db = dbCon

    def popCbo(self, objCombo, tSql, isfetchAll):
        
   
        fetchValues = sqlFunc.fetchSql(tSql,
                                      isfetchAll)
        objCombo.addItem(" ")
        for row in fetchValues:
            #self.cboLgrCus.addItem(str(row[1]), row[0])
            objCombo.addItem(str(row[1]), row[0])
            print(row)

        print("fillComboDataLedger is working!!")

    def getNextPkey(self,tTargetCol,tTargetTbl,ctrLength,isAlphaNum,leadChr):
   
        try:
            tleftChar = "1"
            tLastChr = "A"
            tLastCtr = 0
            tMaxCtr = 0
          
            if isAlphaNum == False:
                valueReturn = leadChr + tleftChar.rjust(ctrLength, "0")
            else:
                valueReturn = leadChr + tLastChr + tleftChar.rjust(ctrLength - 1, "0")
                tMaxCtr = ("9").rjust(ctrLength - 1, "9")
        except:
            print("Something went wrong")
            return ""
        
        try:
          
            fetchValues = sqlFunc.fetchSql( "SELECT " + tTargetCol + " " +
                                        "FROM " + tTargetTbl + " " +
                                        "WHERE " + tTargetCol + " LIKE '%" + leadChr + "%' " +
                                        "ORDER BY " + tTargetCol + " DESC LIMIT 0,1",
                                        "False")
        
            for row in fetchValues:
                if isAlphaNum == False:
                    lenght = len(leadChr)
                    tLastCtr = row[0][lenght:ctrLength]
                    tLastCtr = tLastCtr + 1
                    valueReturn = leadChr + tLastCtr.rjust(ctrLength, "0")

                else:
                    ignoreChr = len(leadChr) + len(tLastChr)
                    if leadChr == row[0][0:(ignoreChr - 1)]:
                        tLastChr = row[0][len(leadChr): len(leadChr) + len(tLastChr)]
                        tLastCtr = row[0][ignoreChr:len(row[0])]
                        tLastCtr = int(tLastCtr) + 1

                        if  tLastCtr <= int(tMaxCtr):
                            valueReturn = leadChr + tLastChr + str(tLastCtr).rjust(ctrLength - 1, "0")
                        else:
                            tLastChr = chr(ascii(tLastChr) + 1)
                            valueReturn = leadChr + tLastChr + str("1").rjust(ctrLength - 1, "0")
                    else:
                        valueReturn = leadChr + tLastChr + str("1").rjust(ctrLength - 1, "0")

            return valueReturn               
         
        except Exception as e:
            print(getattr(e, 'message', str(e)))
       
    def toMySqldate(self, dateValue):
        pass

   
    def getNewBalance(tTable, tColumn, tValue, tType, tAmount):

        fetchValues= sqlFunc.fetchSql("SELECT " + 
                                      "balance " +
                                      "FROM " + tTable + " " +
                                      "WHERE " + tColumn + "='" + tValue + "' " +
                                      "ORDER BY ctrlNo DESC LIMIT 0,1",
                                      "False"
                                       )

        cleanBalance = ""

        for lastBalance in fetchValues:
            try:
                cleanBalance = lastBalance[0]
            except:
                cleanBalance = 0

        newBalance = ""
        try:
            if tType == "1":
                newBalance = int(cleanBalance) - int(tAmount)
            else:
                newBalance = cleanBalance + tAmount
        except ValueError as ve:
            print(ve)

        #aaa = str(newBalance.replace('-',''))
        if int(newBalance) < 0:
            newBalance = newBalance / -1
        return newBalance
        
       
    def encodeBase64Code(self, dataString):
        #texEncode = self.txtStr1.text()
        
        encodedBytes = base64.b64encode(dataString.encode("utf-8"))
        encodedStr = "$" + str(encodedBytes, "utf-8") + "%"
        return encodedStr
     
        #print(decodedStr)

    def decodeBase64Code(self, dataString):
        
        rawData = dataString
        cleanData = rawData.replace("$","")
        cleanData = cleanData.replace("%","")
        
        print(cleanData)
        decodedBytes = base64.b64decode(cleanData)
        decodedStr = str(decodedBytes, "utf-8")

        self.txtBase64Decode.setText(decodedStr)

    def base64Test(self):    
        rawData = []
        rawData.append("s1:" + self.txtStr1.text())
        rawData.append("s2:" + self.txtStr2.text())
        rawData.append("s3:" + self.txtStr3.text())
        rawData.append("s4:" + self.txtStr4.text())

        str1 = ":"
        xxx = str1.join(rawData)
        #self.txtSortOrder.setText(str(xxx))
      
        encodedBytes1 = base64.b64encode(xxx.encode("utf-8"))
        encodedStr1 = "$" + str(encodedBytes1, "utf-8") + "%"

        #self.txtEncodeSort.setText(encodedStr1)
        
        sample_list = random.sample(rawData,4)

        yyy = str1.join(sample_list)
        #self.txtRandSort.setText(str(yyy))
       
        encodedBytes2 = base64.b64encode(yyy.encode("utf-8"))
        encodedStr2 = "$" + str(encodedBytes2, "utf-8") + "%"

        #self.txtEncodeRand.setText(encodedStr2)

        decodedBytes1 = base64.b64decode(encodedStr1)
        decodedStr1 = str(decodedBytes1, "utf-8")

        #self.txtDecodeSort.setText(decodedStr1)

        decodedBytes2 = base64.b64decode(encodedStr2)
        decodedStr2 = str(decodedBytes2, "utf-8")

        #self.txtDecodeRand.setText(decodedStr2)    

    