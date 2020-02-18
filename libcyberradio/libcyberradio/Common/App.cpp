/***************************************************************************
 * \file App.h
 *
 * \brief Defines basic application-level constructs.
 *
 * \author DA
 * \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.
 *
 */

#include "LibCyberRadio/Common/App.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <stdlib.h>
#include <getopt.h>


namespace LibCyberRadio
{

    ///////////////////////////////////////////////////////////////////////
    // AppOption
    ///////////////////////////////////////////////////////////////////////

    int AppOption::TYPE_NONE = 0;
    int AppOption::TYPE_INTEGER = 1;
    int AppOption::TYPE_FLOAT = 2;
    int AppOption::TYPE_DOUBLE = 3;
    int AppOption::TYPE_STRING = 4;
    int AppOption::TYPE_BOOLEAN = 5;
    int AppOption::TYPE_BOOLEAN_SET_TRUE = 6;
    int AppOption::TYPE_BOOLEAN_SET_FALSE = 7;

    AppOption::AppOption()
    {
        valueType = TYPE_NONE;
        valuePtr = (void*)0;
        showDefault = false;
    }

    AppOption::AppOption(const std::string& shortName, const std::string& longName,
            int valueType, void *valuePtr,
            const std::string& helpArgName, const std::string& helpText,
            bool showDefault)
    {
        this->shortName = shortName;
        this->longName = longName;
        this->valueType = valueType;
        this->valuePtr = valuePtr;
        this->helpArgName = helpArgName;
        this->helpText = helpText;
        this->showDefault = showDefault;
    }

    AppOption::AppOption(const AppOption& opt)
    {
        this->shortName = opt.shortName;
        this->longName = opt.longName;
        this->valueType = opt.valueType;
        this->valuePtr = opt.valuePtr;
        this->helpArgName = opt.helpArgName;
        this->helpText = opt.helpText;
        this->showDefault = opt.showDefault;
    }

    AppOption& AppOption::operator=(const AppOption& opt)
    {
        if ( this != &opt )
        {
            this->shortName = opt.shortName;
            this->longName = opt.longName;
            this->valueType = opt.valueType;
            this->valuePtr = opt.valuePtr;
            this->helpArgName = opt.helpArgName;
            this->helpText = opt.helpText;
            this->showDefault = opt.showDefault;
        }
        return *this;
    }

    AppOption::~AppOption()
    {
    }



    ///////////////////////////////////////////////////////////////////////
    // AppHelpTextFormatter
    ///////////////////////////////////////////////////////////////////////

    AppHelpTextFormatter::AppHelpTextFormatter(int displayWidth)
    {
        _maxOptionWidth = 5;
        _displayWidth = displayWidth;
    }

    AppHelpTextFormatter::~AppHelpTextFormatter()
    {
    }

    void AppHelpTextFormatter::addPreOptionText(const std::string& text)
    {
        if ( text != "" )
            _preOptionText.push_back(text);
    }

    void AppHelpTextFormatter::addOptionText(const std::string& option,
            const std::string& text)
    {
        if ( option != "" )
        {
            _options.push_back(option);
            _optionText.push_back(text);
            if ( (int)option.length() > _maxOptionWidth )
                _maxOptionWidth = option.length();
        }
    }

    void AppHelpTextFormatter::addPostOptionText(const std::string& text)
    {
        if ( text != "" )
            _postOptionText.push_back(text);
    }

    std::string AppHelpTextFormatter::getFormattedText()
    {
        std::ostringstream oss, ossTmp;
        // Format pre-option text
        for (BasicStringListIterator it = _preOptionText.begin(); it != _preOptionText.end();
                it++)
        {
            oss << wordWrappedText(*it, _displayWidth, 0);
        }
        // Format option text
        for (BasicStringListIterator ito = _options.begin(), itt = _optionText.begin();
                ito != _options.end();
                ito++, itt++)
        {
            ossTmp.str("");
            ossTmp.clear();
            ossTmp << std::left << std::setw(_maxOptionWidth) << *ito
                    << std::setw(0) << "  "
                    << std::setw(0) << *itt;
            oss << wordWrappedText(ossTmp.str(), _displayWidth, _maxOptionWidth + 2);
        }
        // Format post-option text
        for (BasicStringListIterator it = _postOptionText.begin(); it != _postOptionText.end();
                it++)
        {
            oss << wordWrappedText(*it, _displayWidth, 0);
        }
        return oss.str();
    }

    std::string AppHelpTextFormatter::wordWrappedText(const std::string& text, int width,
            int hangingIndent)
    {
        std::string ret;
        std::string hangingIndentText(hangingIndent, ' ');
        BasicStringList textLines = Pythonesque::Split(text, "\n");
        for (BasicStringListIterator itl = textLines.begin(); itl != textLines.end(); itl++)
        {
            if ( itl == textLines.begin() )
            {
                std::string::size_type curPos = 0;
                int curLine = 0;
                BasicStringList words = Pythonesque::Split(*itl, " ");
                for (BasicStringListIterator itw = words.begin(); itw != words.end(); itw++)
                {
                    // See if printing the next word will go beyond the allowed width
                    if ( curPos + 1 + itw->length() > (std::string::size_type)width )
                    {
                        ret.append("\n");
                        curLine++;
                        // apply hanging indent if needed
                        if ( curLine != 0 )
                        {
                            ret.append(hangingIndentText);
                            curPos = hangingIndentText.length();
                        }
                        // then print the word
                        ret.append(*itw);
                        curPos += itw->length();
                    }
                    else
                    {
                        // Print a space then print the word
                        if (curPos != 0)
                            ret.append(" ");
                        ret.append(*itw);
                        curPos += itw->length() + 1;
                    }
                }
                ret.append("\n");
            }
            else
            {
                ret.append( wordWrappedText(*itl, width, hangingIndent) );
            }
        }
        if ( textLines.size() == 0 )
            ret.append("\n");
        return ret;
    }


    ///////////////////////////////////////////////////////////////////////
    // AppOptionParser
    ///////////////////////////////////////////////////////////////////////

    AppOptionParser::AppOptionParser()
    {
        _allowUnknownOption = false;
        _displayWidth = 75;
        // Configure options that we support automatically:
        // --help
        addOption("", "help", AppOption::TYPE_NONE, (void*)0, "",
                "Print this help text", false);
        // --version
        addOption("", "version", AppOption::TYPE_NONE, (void*)0, "",
                "Print version information and exit", false);
        // Dispatch map for option handler functions.  Each option type
        // (AppOption::TYPE_* constant) should have a corresponding handler
        // function.
        // To add a new option type:
        // (1) Define a member function with this signature to handle that
        // option type:
        //        int handler(int optindex, const std::string& optarg);
        // (2) Add the new handler the dispatch map below.
        _optionHelpers[AppOption::TYPE_NONE] = &AppOptionParser::handleOptionNone;
        _optionHelpers[AppOption::TYPE_INTEGER] = &AppOptionParser::handleOptionInt;
        _optionHelpers[AppOption::TYPE_FLOAT] = &AppOptionParser::handleOptionFloat;
        _optionHelpers[AppOption::TYPE_DOUBLE] = &AppOptionParser::handleOptionDouble;
        _optionHelpers[AppOption::TYPE_STRING] = &AppOptionParser::handleOptionString;
        _optionHelpers[AppOption::TYPE_BOOLEAN] = &AppOptionParser::handleOptionBool;
        _optionHelpers[AppOption::TYPE_BOOLEAN_SET_TRUE] = &AppOptionParser::handleOptionBooleanSetTrue;
        _optionHelpers[AppOption::TYPE_BOOLEAN_SET_FALSE] = &AppOptionParser::handleOptionBooleanSetFalse;
    }

    AppOptionParser::~AppOptionParser()
    {
    }

    void AppOptionParser::addOption(const AppOption& opt)
    {
        _optionList.push_back( opt );
    }

    void AppOptionParser::addOption(const std::string& shortName,
            const std::string& longName,
            int valueType, void *valuePtr,
            const std::string& helpArgName, const std::string& helpText,
            bool showDefault)
    {
        addOption( AppOption(shortName, longName, valueType, valuePtr,
                helpArgName, helpText, showDefault) );
    }

    void AppOptionParser::allowUnknownOption(bool allow)
    {
        _allowUnknownOption = allow;
    }

    void AppOptionParser::setDescription(const std::string& description)
    {
        _description = description;
    }

    void AppOptionParser::setDisplayWidth(int displayWidth)
    {
        _displayWidth = displayWidth;
    }

    void AppOptionParser::setEpilogText(const std::string& epilogText)
    {
        _epilogText = epilogText;
    }

    void AppOptionParser::setExecutable(const std::string& executable)
    {
        _executable = executable;
    }

    void AppOptionParser::setUnparsedArgText(const std::string& unparsedArgText)
    {
        _unparsedArgText = unparsedArgText;
    }

    void AppOptionParser::setVersion(const std::string& version)
    {
        _version = version;
    }

    int AppOptionParser::parse(int argc, char** argv)
    {
        int ret = 0;
        // Form short argument list and long option structure list
        std::string shargs;
        struct option longOptions[_optionList.size() + 1];
        for (int i = 0; i < (int)_optionList.size(); i++)
        {
            // If a long option has a corresponding short option,
            // set the return value to the short option character.
            if ( _optionList[i].shortName.length() == 1 )
            {
                shargs.append(_optionList[i].shortName);
                if ( optionValueArg(_optionList[i].valueType) )
                    shargs.append(":");
                longOptions[i].val = (int)_optionList[i].shortName[0];
            }
            // Otherwise, encode the index in the return value.
            else
            {
                longOptions[i].val = 32768+i;
            }
            longOptions[i].name = _optionList[i].longName.c_str();
            longOptions[i].has_arg = optionValueArg(_optionList[i].valueType);
            longOptions[i].flag = (int*)0;
        }
        // Terminate long option structure list with an empty element
        longOptions[_optionList.size()].name = (char*)0;
        longOptions[_optionList.size()].has_arg = 0;
        longOptions[_optionList.size()].flag = (int*)0;
        longOptions[_optionList.size()].val = 0;
#ifdef DEBUG
        std::cerr << "[DBG] Short option list: " << shargs << std::endl;
#endif

        // Parse options
        int opt = 0;
        int optindex = 0;
        while (1)
        {
            opt = getopt_long(/* int */ argc, /* char * const argv[] */ argv,
                    /* const char *optstring */ shargs.c_str(),
                    /* const struct option *longopts */ (const struct option *)longOptions,
                    /* int *longindex */ &optindex);
            if (opt == -1)
                break;
#ifdef DEBUG
            std::cerr << "Option parsed: " << opt << " (" << (char)opt << ")" << std::endl;
#endif

            switch(opt)
            {
                case '?':
                    // Option is unknown.
                    if ( !_allowUnknownOption )
                        ret = 2;
                    break;
                default:
                    // Option is known but we haven't handled it yet.
                    ret = handleOptionReturn(opt, optarg ? optarg : "");
                    if ( ret == 1 )
                        std::cerr << "ERROR: Improperly formatted argument!" << std::endl;
                    break;
            }
            if ( ret != 0 )
                break;
        }
        // Collect unparsed arguments.  Use of unparsed arguments is application-specific.
        if ( (ret == 0) && (optind < argc) )
        {
            while (optind < argc)
                unparsedArgs.push_back( argv[optind++] );
        }

        return ret;
    }

    int AppOptionParser::handleOptionReturn(int opt, const std::string& optarg)
    {
        int ret = 0;
        // We need to find the option index that corresponds to our option
        // return value.
        int our_optindex = -1;
        // -- Short options, and long options w/ short options, have return
        //    values < 32768; return value = short option value
        if ( opt < 32768 )
        {
            // Find the option where return value = short option value
            for (int i = 0; i < (int)_optionList.size(); i++)
            {
                if ( (_optionList[i].shortName.length() == 1) &&
                        (_optionList[i].shortName[0] == (char)opt) )
                {
                    our_optindex = i;
                    break;
                }
            }
        }
        // -- Long options w/o short options have return values >= 32768; option
        //    index = return value - 32768
        else
        {
            our_optindex = opt - 32768;
        }
        // Dispatch option handler if we can
        if ( our_optindex != -1 )
        {
            if ( _optionList[our_optindex].longName == "version" ) // Version information request
            {
                std::cerr << _description << ", Version " << _version << std::endl;
                ret = 3;
            }
            else if ( _optionList[our_optindex].longName == "help" )   // Help requested
            {
                printUsage();
                ret = 2;
            }
            else if ( _optionHelpers.count(_optionList[our_optindex].valueType) > 0 )
            {
                ret = (this->*_optionHelpers[_optionList[our_optindex].valueType])(our_optindex, optarg);
            }
            else
                ret = 1;
        }
        else
            ret = 1;
        return ret;
    }

    void AppOptionParser::printUsage()
    {
        std::ostringstream ossPre, ossPost;
        AppHelpTextFormatter fmtr(_displayWidth);
        ossPre << _description << ", Version " << _version << "\n\n" << "Usage:\n" << _executable;
        if ( _optionList.size() > 0 )
            ossPre << " [options]";
        if ( _unparsedArgText.length() > 0 )
            ossPre << " " << _unparsedArgText;
        ossPre << "\n\n";
        if ( _optionList.size() > 0 )
        {
            ossPre << "Options:\n\n";
            std::string opt, optText;
            for (int i = 0; i < (int)_optionList.size(); i++)
            {
                opt = "";
                if ( _optionList[i].shortName.length() == 1 )
                {
                    opt.append("-");
                    opt.append(_optionList[i].shortName);
                    if ( optionValueArg(_optionList[i].valueType) > no_argument )
                    {
                        opt.append(" ");
                        opt.append(_optionList[i].helpArgName);
                    }
                }
                if ( _optionList[i].longName.length() > 0 )
                {
                    if ( opt != "" )
                        opt.append(", ");
                    opt.append("--");
                    opt.append(_optionList[i].longName);
                    if ( optionValueArg(_optionList[i].valueType) > no_argument )
                    {
                        opt.append("=");
                        opt.append(_optionList[i].helpArgName);
                    }
                }
                // std::cerr << std::left << std::setw(25) << opt
                // << std::setw(0) << "  "
                // << std::setw(0) << _optionList[i].help_text
                // << "\n";
                optText = _optionList[i].helpText;
                optText.append( getDefault(_optionList[i]) );
                fmtr.addOptionText(opt, optText);
            }
        }
        if ( _epilogText.length() > 0 )
            ossPost << "\n" << _epilogText << "\n";
        fmtr.addPreOptionText(ossPre.str());
        fmtr.addPostOptionText(ossPost.str());
        //std::cerr << "[DBG] Formatter loaded" << std::endl;
        std::cerr << fmtr.getFormattedText() << std::endl;
    }

    int AppOptionParser::optionValueArg(int valueType)
    {
        int ret = no_argument;
        if ( (valueType >= AppOption::TYPE_INTEGER) &&
                (valueType <= AppOption::TYPE_BOOLEAN) )
            ret = required_argument;
        return ret;
    }

    std::string AppOptionParser::getDefault(const AppOption& opt)
    {
        std::ostringstream oss;
        int *iptr;
        float *fptr;
        double *dptr;
        bool *bptr;
        std::string *sptr;
        if ( opt.showDefault && (opt.valuePtr != (void*)0) )
        {
            oss << "  Default: ";
            if ( opt.valueType == AppOption::TYPE_INTEGER )
            {
                iptr = (int *)opt.valuePtr;
                oss << *iptr << ".";
            }
            else if ( opt.valueType == AppOption::TYPE_FLOAT )
            {
                fptr = (float *)opt.valuePtr;
                oss << *fptr << ".";
            }
            else if ( opt.valueType == AppOption::TYPE_DOUBLE )
            {
                dptr = (double *)opt.valuePtr;
                oss << *dptr << ".";
            }
            else if ( opt.valueType == AppOption::TYPE_STRING )
            {
                sptr = (std::string *)opt.valuePtr;
                oss << *sptr << ".";
            }
            else if ( (opt.valueType >= AppOption::TYPE_BOOLEAN) &&
                    (opt.valueType <= AppOption::TYPE_BOOLEAN_SET_FALSE) )
            {
                bptr = (bool *)opt.valuePtr;
                oss << (*bptr ? "True" : "False") << ".";
            }
            else
            {
                oss << "None.";
            }
        }
        return oss.str();
    }

    int AppOptionParser::handleOptionNone(int optindex, const std::string& optarg)
    {
        return 0;
    }

    int AppOptionParser::handleOptionInt(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            char *endptr;
            int *vptr = (int *)_optionList[optindex].valuePtr;
            int tmp = (int)strtol(optarg.c_str(), &endptr, 10);
            if ( *endptr == '\0' )
                *vptr = tmp;
            else
                ret = 1;
        }
        return ret;
    }

    int AppOptionParser::handleOptionFloat(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            char *endptr;
            float *vptr = (float *)_optionList[optindex].valuePtr;
            float tmp = (float)strtod(optarg.c_str(), &endptr);
            if ( *endptr == '\0' )
                *vptr = tmp;
            else
                ret = 1;
        }
        return ret;
    }

    int AppOptionParser::handleOptionDouble(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            char *endptr;
            double *vptr = (double *)_optionList[optindex].valuePtr;
            double tmp = strtod(optarg.c_str(), &endptr);
            if ( *endptr == '\0' )
                *vptr = tmp;
            else
                ret = 1;
        }
        return ret;
    }

    int AppOptionParser::handleOptionString(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            std::string *vptr = (std::string *)_optionList[optindex].valuePtr;
            *vptr = optarg;
        }
        return ret;
    }

    int AppOptionParser::handleOptionBool(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            std::string val = optarg;
            bool *vptr = (bool *)_optionList[optindex].valuePtr;
            std::transform(val.begin(), val.end(), val.begin(), ::tolower);
            if ( (val == "true") || (val == "yes") || (val == "on") || (val == "1") )
                *vptr = true;
            else if ( (val == "false") || (val == "no") || (val == "off") || (val == "0") )
                *vptr = false;
            else
                ret = 1;
        }
        return ret;
    }

    int AppOptionParser::handleOptionBooleanSetTrue(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            bool *vptr = (bool *)_optionList[optindex].valuePtr;
            *vptr = true;
        }
        return ret;
    }

    int AppOptionParser::handleOptionBooleanSetFalse(int optindex, const std::string& optarg)
    {
        int ret = 0;
        if ( _optionList[optindex].valuePtr != (void*)0 )
        {
            bool *vptr = (bool *)_optionList[optindex].valuePtr;
            *vptr = false;
        }
        return ret;
    }



    ///////////////////////////////////////////////////////////////////////
    // App
    ///////////////////////////////////////////////////////////////////////

    App::App ()
    {
        description = "Generic Application";
        version = "0.0.1";
    }

    int App::run(int argc, char *argv[])
    {
        defineOptions(argv[0]);
        int ret = parseCommandLine(argc, argv);
        if ( ret == 0 )
            ret = mainLoop();
        return ret;
    }

    void App::defineOptions(const char *argv0)
    {
        // Base-class implementation configures basic app info and usage info
        _optParser.setDescription(description);
        _optParser.setVersion(version);
        _optParser.setExecutable(argv0);
        _optParser.setUnparsedArgText("");
        _optParser.setEpilogText("");
        // Derived classes should call base-class version, then extend/override with their
        // own supported options.
    }

    int App::mainLoop()
    {
        // Base-class implementation does nothing; derived classes should override
        // with their own implementations.
        int ret = 0;
        return ret;
    }

    int App::parseCommandLine(int argc, char* argv[])
    {
        return _optParser.parse(argc, argv);
    }

}
