# callbackexception.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides the CallbackException class to report an exception
and optionally display it's details before stopping the application.
"""


class CallbackException(object):
    """The CallbackException class provides methods to report exceptions in
    a modal dialogue and 'do nothing' wrappers for tkinter callbacks and
    methods run in a separate thread.

    Subclasses should override these methods to customise the reporting of
    exceptions.
    
    """

    def report_exception(self, root=None, title=None, message=None):
        """Report the exception in a modal dialogue.

        root - usually the application toplevel widget
        title - usually the application name
        message - usually the exception traceback
        """

        # If root is left as None it is possible to generate the following on
        # stderr, maybe it's stdout, presumably from _tkinter:
        #
        # bgerror failed to handle background error.
        # Original Error:
        # ...
        #
        # by destroying the application toplevel before the exception report
        # toplevel(s).
        #
        # This may result in Microsoft Windows User Access Control preventing
        # an attempt to write an errorlog to the application folder in Program
        # Files by a py2exe generated executable.  Such attempts cause a
        # reasonable, but possibly worrying, error information dialogue to be
        # launched.

        import traceback
        import tkinter
        import tkinter.messagebox

        # At 2009-08-01 calling tkMessageBox.askyesno and so on does not work
        # on Python2.6: s == YES compares booleanString with str
        # but calling _show works (as it does in tkMessageBox.py test stuff)
        # tkFileDialog functions seem ok

        # This method added at 30 August 2017 when moving dialogues module from
        # solentware_base.tools to solentware_misc.workarounds to avoid a
        # circular import loop between solentware_grid and solentware_misc.

        def askyesno(title=None, message=None, **options):
            try:
                s = tkinter.messagebox._show(
                    title,
                    message,
                    tkinter.messagebox.QUESTION,
                    tkinter.messagebox.YESNO,
                    **options)
                return str(s) == tkinter.messagebox.YES
            except tkinter.TclError as error:
                if str(error) != ''.join(("can't invoke ",
                                          '"grab" command:  ',
                                          'application has been destroyed')):
                    raise

        if title is None:
            title = 'Exception Report'
        if message is None:
            message = ''.join(
                ('An exception has occured.\n\nClick "Yes" to see ',
                 'the detail\nor "No" to quit the application',
                 ))

        if root:
            try:
                pending = root.tk.call('after', 'info')
                for p in pending.split():
                    try:
                        root.after_cancel(p)
                    except:
                        pass
            except:
                pass
            
        if root is None:
            dialtop = tkinter.Tk()
        else:
            dialtop = root
        try:
            if not askyesno(
                master=dialtop,
                title=title,
                message=message,
                ):
                dialtop.destroy()
                raise SystemExit('Do not show exception report')
        except:
            # A non-error example, in context, is two failing after_idle calls.
            # Then click Quit on the second report before clicking No on the
            # first askyesno. The second askyesno has not been invoked yet.
            # If it is an error there is nothing realistic that can be done for
            # the application error being reported.
            try:
                dialtop.destroy()
            except:
                pass
            raise SystemExit('Exception in exception report dialogue')

        if root is None:
            top = dialtop
        else:
            top = tkinter.Toplevel(master=root)
        # It may be ok to allow the application to respond to keyboard and
        # pointer actions but exceptions when exceptions have already occurred
        # could loop indefinitely or be allowed to escape into Tkinter.  This
        # module is about stopping the latter; and it is confusing to say
        # 'something is wrong' and allow normal actions to proceed.
        # So grab_set.
        top.grab_set()
        top.wm_title(string=title)
        quit_ = tkinter.Button(master=top, text='Quit')
        quit_.pack(side=tkinter.BOTTOM)
        report = tkinter.Text(master=top, wrap='word')
        quit_.configure(command=top.destroy)
        scrollbar = tkinter.Scrollbar(
            master=top, orient=tkinter.VERTICAL, command=report.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        report.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
        report.configure(yscrollcommand=scrollbar.set)
        report.insert(tkinter.END, traceback.format_exc())
        top.wait_window()
        # Without the delete pending 'after' commands at start of method this
        # raise does not seem to be needed to quit the application.
        raise SystemExit('Dismiss exception report')

    def try_command(self, method, widget):
        """Return the method.

        Subclasses may override this method to intercept errors in tkinter
        callbacks and implement custom error handling which replaces the
        default output to stderr.

        """
        return method

    def try_event(self, method):
        """Return the method.

        Subclasses may override this method to intercept errors in tkinter
        callbacks and implement custom error handling which replaces the
        default output to stderr.

        """
        return method

    def try_thread(self, method, widget):
        """Return the method.

        Subclasses may override this method to intercept errors in threaded
        activities and implement custom error handling which replaces the
        default output to stderr.

        """
        return method

