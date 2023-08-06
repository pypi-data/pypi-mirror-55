def countActiveWell(well):
    output_well = [x for x in well if x["IS_ACTIVE"] == False]
    # count all well retrieved from API
    print("total well count:" , len(well))
    # count well which is actived
    print("active well count:" , len(output_well))