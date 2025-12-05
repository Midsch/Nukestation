

info = []

patternList = [{'patternStart': 'notice: Starting round',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'notice: Starting pass',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'notice: Finished pass',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'notice: Finished final round',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'notice: Blanking device',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'notice: Verifying that',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 9,
                'type': 'notice',
               }, {
                'patternStart': 'notice: [SUCCESS] Verified that',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 9,
                'type': 'notice',
               }, {
                'patternStart': 'notice: [SUCCESS] Blanked device',
                'patternEnd': 'deviceName',
                'shiftStart': 8,
                'shiftEnd': 0,
                'type': 'notice',
               }, {
                'patternStart': 'Nwipe successfully completed',
                'patternEnd': 'false',                
                 'shiftStart': 0,
                 'shiftEnd': 0,
                 'type': 'success',
               }, {
                'patternStart': 'fatal: Nwipe exited with errors on device',
                'patternEnd': 'deviceName',                
                 'shiftStart': 7,
                 'shiftEnd': 0,
                 'type': 'info',
               }, {
                'patternStart': 'Nwipe exited with errors',
                'patternEnd': 'false',                
                 'shiftStart': 0,
                 'shiftEnd': 0,
                 'type': 'error',
               }, {
                'patternStart': 'info:',
                'patternEnd': 'deviceName',                
                 'shiftStart': 16,
                 'shiftEnd': 7,
                 'type': 'progress',
               }]



def accessFileByLine(logfileDir, logfileName, deviceName):
    global info
    info = []

    #try:
    file = open(logfileDir + logfileName, 'r')
    
    for line in file:
        extractInfo(line, deviceName)

    file.close()
    #print(info)
    return info
    #except:
    #    print('No file found')


def extractInfo(line, deviceName):
    global patternList
    global info

    for pattern in patternList:
        indicatorStart = int(line.find(pattern['patternStart']))

        if indicatorStart > -1 and pattern['patternEnd'] == 'false':
            indicatorEnd = indicatorStart + len(pattern['patternStart']) + pattern['shiftEnd']
        elif indicatorStart > -1 and pattern['patternEnd'] == 'deviceName':
            if line.find(deviceName) == -1:
                indicatorStart = -1
            else:
                indicatorEnd = int(line.find(deviceName) + len(deviceName))  + pattern['shiftEnd']

        if indicatorStart != -1:
            indexStart = indicatorStart + pattern['shiftStart']
            indexEnd = indicatorEnd

            if pattern['type'] == 'progress':
                #print('patternStart: ' + pattern['patternStart'])
                #print('info: ' + line[indexStart:indexEnd])
                if info[0]['type'] != 'progress':
                    info.insert(0, {'text': line[indexStart:indexEnd], 'type': pattern['type']})
                elif info[0]['type'] == 'progress':
                    info.pop(0)
                    info.insert(0, {'text': line[indexStart:indexEnd], 'type': pattern['type']})
            else:
                info += [{'text': line[indexStart:indexEnd], 'type': pattern['type']}]
            
