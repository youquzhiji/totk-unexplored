#include "Accounts.h"

#include <string.h>
#include <stdio.h>

AccountUid Accounts::RequestProfileSelection()
{
    struct UserReturnData{
        u64 result;
        AccountUid UID;
    } PACKED;

    struct UserReturnData outdata;

    AppletHolder aph;
    AppletStorage ast;
    AppletStorage hast1;
    LibAppletArgs args;

    u8 indata[0xA0] = { 0 };
    indata[0x96] = 1;

    appletCreateLibraryApplet(&aph, AppletId_LibraryAppletPlayerSelect, LibAppletMode_AllForeground);
    libappletArgsCreate(&args, 0);
    libappletArgsPush(&args, &aph);

    appletCreateStorage(&hast1, 0xA0);

    appletStorageWrite(&hast1, 0, indata, 0xA0);
    appletHolderPushInData(&aph, &hast1);
    appletHolderStart(&aph);

    while (appletHolderWaitInteractiveOut(&aph));

    appletHolderJoin(&aph);
    appletHolderPopOutData(&aph, &ast);
    appletStorageRead(&ast, 0, &outdata, 24);

    appletHolderClose(&aph);
    appletStorageClose(&ast);
    appletStorageClose(&hast1);

    return outdata.UID;
}

// doesn't work
std::string Accounts::GetNickname(AccountUid uid)
{
    char nickname[0x21];

    AccountProfile profile;
    AccountProfileBase profileBase;

    memset(&profileBase, 0, sizeof(profileBase));

    Result rc = accountGetProfile(&profile, uid);
    if (R_FAILED(rc))
        printf("accountGetProfile() failed\n");

    rc = accountProfileGet(&profile, NULL, &profileBase);
    if (R_FAILED(rc))
        printf("accountProfileGet() failed\n");

    memset(nickname,  0, sizeof(nickname));
    strncpy(nickname, profileBase.nickname, sizeof(nickname) - 1);//Copy the nickname elsewhere to make sure it's NUL-terminated.

    return std::string(nickname);
}