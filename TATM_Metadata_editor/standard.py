# -*- coding: utf-8 -*-

#******************************************************************************

class MetaInfoStandard:
  UNKNOWN, ISO19115, FGDC, DC = range(4)

  @staticmethod
  def tryDetermineStandard(metaProvider):
    text = metaProvider.getMetadata()
    #print "TryDetStd ", text, " Text"

    # simple test for iso doc
    if text.find("MD_Metadata") >= 0 or text.find("MI_Metadata") >= 0:
        return MetaInfoStandard.ISO19115

    # simple test for fgdc doc
    if text.find("idinfo") >= 0 and text.find("metainfo") >= 0:
        return MetaInfoStandard.FGDC

    # only iso and fgdc support now
    return MetaInfoStandard.UNKNOWN
