/***************************************************************************
 * \file App.h
 *
 * \brief Defines basic application-level constructs.
 *
 * \author DA
 * \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_APP_H
#define INCLUDED_LIBCYBERRADIO_APP_H

#include <string>
#include <map>
#include <getopt.h>
#include "LibCyberRadio/Common/BasicList.h"


/**
 * \brief Defines functionality for LibCyberRadio applications.
 */
namespace LibCyberRadio
{
    /**
     * \brief Defines a command-line option that is supported by an application.
     */
    class AppOption
    {
        public:
            /**
             * \brief Constructs an empty AppOption object.
             */
            AppOption();
            /**
             * \brief Constructs an AppOption object from initial parameters.
             *
             * \param shortName
             * Short option name, without leading hyphen.  If empty,
             * this option does not support short format.
             * \param longName
             * Long option name, without leading hyphens.  If empty,
             * this option does not support long format.
             * \param valueType
             * Type of value that this option sets.  Must be one of the
             * AppOption::TYPE_* constants.
             * \param valuePtr
             * Pointer to a variable that holds the option value.
             * \param helpArgName
             * Option argument name to display in the help text.
             * \param helpText
             * Option help text.
             * \param showDefault
             * Whether or not to show the default value of the option
             * in the help text.  The default value will be appended to
             * the help text given in helpText.
             */
            AppOption(const std::string& shortName, const std::string& longName,
                    int valueType, void *valuePtr,
                    const std::string& helpArgName, const std::string& helpText,
                    bool showDefault);
            /**
             * \brief Constructs an AppOption object as a copy of another.
             *
             * \param opt
             * The AppOption object being copied.
             */
            AppOption(const AppOption& opt);
            /**
             * \brief Makes one AppOption object equivalent to another.
             *
             * \param opt
             * The AppOption object being copied.
             */
            virtual AppOption& operator=(const AppOption& opt);
            /**
             * \brief Destroys an AppOption object.
             */
            virtual ~AppOption();

        public:
            /**
             * \brief Short option name, without leading hyphen.  If empty, this option does
             * not support short format.
             */
            std::string shortName;
            /**
             * \brief Long option name, without leading hyphens.  If empty, this option does
             * not support long format.
             */
            std::string longName;
            /**
             * \brief Type of value that this option sets.  Must be one of the
             * AppOption::TYPE_* constants.
             */
            int valueType;
            /**
             * \brief Pointer to a variable that holds the option value.
             */
            void *valuePtr;
            /**
             * \brief Option argument name to display in the help text.
             */
            std::string helpArgName;
            /**
             * \brief Option help text.
             */
            std::string helpText;
            /**
             * \brief Show the default value in the option help text.  The default value
             * is obtained from the variable pointed to by valuePtr.
             */
            bool showDefault;

        public:
            /**
             * \brief Option does not set a value.
             */
            static int TYPE_NONE;
            /**
             * \brief Option sets an integer value.
             */
            static int TYPE_INTEGER;
            /**
             * \brief Option sets a floating-point value.
             */
            static int TYPE_FLOAT;
            /**
             * \brief Option sets a double-precision floating-point value.
             */
            static int TYPE_DOUBLE;
            /**
             * \brief Option sets a string value.
             */
            static int TYPE_STRING;
            /**
             * \brief Option explicitly sets a boolean value.
             */
            static int TYPE_BOOLEAN;
            /**
             * \brief Option sets a boolean value that is False by default but becomes True
             * if this option is specified.
             */
            static int TYPE_BOOLEAN_SET_TRUE;
            /**
             * \brief Option sets a boolean value that is True by default but becomes False
             * if this option is specified.
             */
            static int TYPE_BOOLEAN_SET_FALSE;
    };


    /**
     * \brief Defines a list of AppOption objects.
     */
    typedef BASIC_LIST_CONTAINER<AppOption> AppOptionList;


    /**
     * \brief Formats help text for display on the screen.
     */
    class AppHelpTextFormatter
    {
        public:
            /**
             * \brief Constructs an AppHelpTextFormatter object.
             *
             * \param displayWidth
             * The width of the area in which to format the text, in characters.
             */
            AppHelpTextFormatter(int displayWidth = 75);
            /**
             * \brief Destroys an AppHelpTextFormatter object.
             */
            virtual ~AppHelpTextFormatter();
            /**
             * \brief Adds text that gets displayed before the list of options.
             *
             * If addPreOptionText() is called multiple times, the formatter will
             * add the text to an internal store, and display the text in the order
             * in which it is added.
             *
             * \param text
             * The text to add.  This text may be divided into separate lines via
             * newline (\n) characters.
             *
             */
            virtual void addPreOptionText(const std::string& text);
            /**
             * \brief Adds an option and its help text to the list of options.
             *
             * If addOptionText() is called multiple times, the formatter will
             * add the option and its help text to the list, and display the text in
             * the order in which it is added.
             *
             * \param option
             * The option.  This text should describe any supported forms (short
             * and/or long), as well as any arguments required by the option.
             * \param text
             * The help text for the option.  This text may be divided into separate
             * lines via newline (\n) characters.
             */
            virtual void addOptionText(const std::string& option, const std::string& text);
            /**
             * \brief Adds text that gets displayed after the list of options.
             *
             * If addPreOptionText() is called multiple times, the formatter will
             * add the text to an internal store, and display the text in the order
             * in which it is added.
             *
             * \param text
             * The text to add.  This text may be divided into separate lines via
             * newline (\n) characters.
             *
             */
            virtual void addPostOptionText(const std::string& text);
            /**
             * \brief Gets the formatted help text.
             *
             * \return A string containing the formatted help text.
             */
            virtual std::string getFormattedText();

        protected:
            // Wraps the given text to the specified width (in characters), applying
            // the given hanging indent (in characters) to each line after the first.
            virtual std::string wordWrappedText(const std::string& text, int width,
                    int hangingIndent);

        protected:
            BasicStringList _preOptionText;
            BasicStringList _options;
            BasicStringList _optionText;
            BasicStringList _postOptionText;
            int _maxOptionWidth;
            int _displayWidth;
    };


    /**
     * \brief Parses command-line options supported by the application.
     *
     * The option parser defines the following options by default:
     * --help         Prints help text and exits
     * --version      Prints version information and exits
     *
     */
    class AppOptionParser
    {
        public:
            /**
             * \brief Constructs an AppOptionParser object.
             */
            AppOptionParser();
            /**
             * \brief Destroys an AppOptionParser object.
             */
            virtual ~AppOptionParser();
            /**
             * \brief Determines whether or not the parser will allow unknown options to
             * pass through the parser without generating an error.
             *
             * The default behavior is to disallow unknown options.
             *
             * \param allow
             * Whether or not to allow unknown options to pass through.
             */
            void allowUnknownOption(bool allow = true);
            /**
             * \brief Sets the portion of the usage information where the application
             * description is displayed.
             *
             * \param description
             * The application description.
             */
            void setDescription(const std::string& description);
            /**
             * \brief Sets the display width of the usage information.
             *
             * \param displayWidth
             * The display width, in characters.
             */
            void setDisplayWidth(int displayWidth = 75);
            /**
             * \brief Sets the epilog portion of the usage information; that is, the part
             * that comes after the list of supported options.
             *
             * The epilog text may be divided into lines via newline (\n)
             * characters.
             *
             * \param epilogText
             * The epilog text.
             */
            void setEpilogText(const std::string& epilogText);
            /**
             * \brief Sets the portion of the usage information where the executable name
             * is displayed.
             *
             * This is usually the contents of argv[0].
             *
             * \param executable
             * The executable name to display.
             */
            void setExecutable(const std::string& executable);
            /**
             * \brief Sets the portion of the usage information that represents the
             * collection of unparsed arguments.
             *
             * \param unparsedArgText
             * The text to display.
             */
            void setUnparsedArgText(const std::string& unparsedArgText);
            /**
             * \brief Sets the portion of the usage information that represents the
             * application version.
             *
             * \param version
             * The application version.
             */
            void setVersion(const std::string& version);
            /**
             * \brief Adds an allowed option to the parser.
             *
             * \param opt
             * An AppOption object describing the option to add to the parser.
             */
            virtual void addOption(const AppOption& opt);
            /**
             * \brief Adds an allowed option to the parser.
             *
             * \param shortName
             * Short option name, without leading hyphen.  If empty,
             * this option does not support short format.
             * \param longName
             * Long option name, without leading hyphens.  If empty,
             * this option does not support long format.
             * \param valueType
             * Type of value that this option sets.  Must be one of the
             * AppOption::TYPE_* constants.
             * \param valuePtr
             * Pointer to a variable that holds the option value.
             * \param helpArgName
             * Option argument name to display in the help text.
             * \param helpText
             * Option help text.
             * \param showDefault
             * Whether or not to show the default value of the option
             * in the help text.  The default value will be appended to
             * the help text given in helpText.
             */
            virtual void addOption(const std::string& shortName, const std::string& longName,
                    int valueType, void *valuePtr,
                    const std::string& helpArgName, const std::string& helpText,
                    bool showDefault);
            /**
             * \brief Parses the command-line options.
             *
             * After parsing, any unparsed arguments are collected in unparsedArgs.
             *
             * \param argc
             * The number of arguments specified on the command line, counting the executable
             * name itself.
             * \param argv
             * The list of arguments specified on the command line, including the executable
             * name itself.
             * \return An integer indicating the success or failure of the parsing operation,
             * as follows:
             * 0 = all options parsed successfully
             * 1 = error encountered in option processing
             * 2 = usage information was requested
             * 3 = version information was requested
             */
            virtual int parse(int argc, char **argv);

        protected:
            // Prints usage information.
            virtual void printUsage();
            // Determines whether an option should have an argument based on its type.
            virtual int optionValueArg(int valueType);
            // Gets the default value for a given option, as a string.
            virtual std::string getDefault(const AppOption& opt);
            // Dispatch function for handling configured options.
            virtual int handleOptionReturn(int opt, const std::string& optarg);
            // Option type handler functions.
            // -- AppOptionValueType::NONE
            virtual int handleOptionNone(int optindex, const std::string& optarg);
            // -- AppOptionValueType::INTEGER
            virtual int handleOptionInt(int optindex, const std::string& optarg);
            // -- AppOptionValueType::FLOAT
            virtual int handleOptionFloat(int optindex, const std::string& optarg);
            // -- AppOptionValueType::DOUBLE
            virtual int handleOptionDouble(int optindex, const std::string& optarg);
            // -- AppOptionValueType::STRING
            virtual int handleOptionString(int optindex, const std::string& optarg);
            // -- AppOptionValueType::BOOLEAN
            virtual int handleOptionBool(int optindex, const std::string& optarg);
            // -- AppOptionValueType::BOOLEAN_SET_TRUE
            virtual int handleOptionBooleanSetTrue(int optindex, const std::string& optarg);
            // -- AppOptionValueType::BOOLEAN_SET_FALSE
            virtual int handleOptionBooleanSetFalse(int optindex, const std::string& optarg);

        public:
            /**
             * \brief The collection of arguments that were not dealt with by the parser during
             * option parsing.
             */
            BasicStringList unparsedArgs;

        protected:
            AppOptionList _optionList;
            std::string _description;
            std::string _version;
            std::string _executable;
            std::string _unparsedArgText;
            std::string _epilogText;
            bool _allowUnknownOption;
            int _displayWidth;
            typedef int (AppOptionParser::*OptionHelper)(int optindex, const std::string& optarg);
            std::map<int, OptionHelper> _optionHelpers;
    };


    /**
     * \brief Provides basic application functionality.
     *
     * Applications using this class as a base should override the following:
     * \li \link description \endlink: The application description.
     * \li \link version \endlink: The application version.
     * \li defineOptions(): Defines which options are supported.
     * \li mainLoop(): Performs application processing.
     *
     * The entry point for running the application processing loop is run().
     */
    class App
    {
        public:
            /**
             * \brief Constructs an App object.
             */
            App();
            /**
             * \brief Destroys an App object.
             */
            virtual ~App() { };
            /**
             * \brief Runs the application.
             *
             * \param argc
             * The number of arguments specified on the command line, counting the executable
             * name itself.
             * \param argv
             * The list of arguments specified on the command line, including the executable
             * name itself.
             * \return An integer whose return value is passed up to the host operating system
             * as a return code.  This is application-dependent, but the following return
             * codes are generated as a result of command-line argument/option processing:
             * \li 1 = error encountered in option processing
             * \li 2 = usage information was requested
             * \li 3 = version information was requested
             */
            virtual int run(int argc, char *argv[]);

        protected:
            /**
             * \brief Defines which command-line options are supported by the application, as
             * well as any help text that is displayed.
             *
             * The option parser, available through member variable \c _optParser, is an
             * AppOptionParser object.
             *
             * \param argv0
             * The name of the executable, as passed into the program via \c argv[0].
             */
            virtual void defineOptions(const char *argv0);
            // .  The return value will
            // be passed up to the host operating system as a return code.
            /**
             * \brief Defines the application's main processing loop.
             *
             * The base-class implementation of this method does nothing, and returns 0.
             * Derived classes must override this method for the application to perform
             * any useful work.
             */
            virtual int mainLoop();
            // Parses command-line options.
            virtual int parseCommandLine(int argc, char *argv[]);

        public:
            /**
             * \brief The application description.
             */
            std::string description;
            /**
             * \brief The application version.
             */
            std::string version;

        protected:
            AppOptionParser _optParser;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_APP_H */

