/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#include "tibb.h"

int cascades_user_main(int argc, char **argv)
{
    int ret = tibb_run("Titanium.API.debug(Titanium.version);", argc, argv);
    return ret;
}
